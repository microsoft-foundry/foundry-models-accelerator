#!/usr/bin/env python
import argparse
import csv
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

API_VERSIONS = [
    "2023-05-01",
    "2023-10-01-preview",
    "2024-02-01",
    "2024-06-01-preview",
]

DEFAULT_TARGET_MODELS = [
    {"ModelName": "gpt-4o", "Versions": ["2025-08-06", "2025-05-13"]},
    {"ModelName": "gpt-4o-mini", "Versions": ["2024-07-18"]},
]

RETIREMENTS_FILE = Path(__file__).with_name("model_retirements.json")


def resolve_az_path():
    az_path = os.environ.get("AZURE_CLI_PATH")
    if az_path:
        return az_path
    return shutil.which("az")


def run_az(args, allow_error=False):
    az_path = resolve_az_path()
    if not az_path:
        raise RuntimeError(
            "Azure CLI not found. Install Azure CLI or set AZURE_CLI_PATH to az.cmd/az.exe."
        )
    result = subprocess.run([az_path, *args], capture_output=True, text=True)
    if result.returncode != 0:
        if allow_error:
            return None
        raise RuntimeError(result.stderr.strip() or "Azure CLI command failed")
    return result.stdout.strip()


def get_default_subscription_id():
    out = run_az(["account", "show", "--query", "id", "-o", "tsv"])
    return out.strip()


def try_list_deployments(resource_id):
    for api in API_VERSIONS:
        try:
            out = run_az(
                [
                    "rest",
                    "--method",
                    "GET",
                    "--uri",
                    f"{resource_id}/deployments?api-version={api}",
                    "-o",
                    "json",
                ],
                allow_error=True,
            )
            if out:
                return json.loads(out)
        except Exception:
            continue
    return None


def enable_diagnostics(resource_id, enable, workspace_id, diag_name):
    if not enable:
        return
    if not workspace_id:
        raise ValueError("EnableDiag set but DiagWorkspaceId is empty.")

    cats_json = run_az(
        [
            "monitor",
            "diagnostic-settings",
            "categories",
            "list",
            "--resource",
            resource_id,
            "-o",
            "json",
        ],
        allow_error=True,
    )
    if not cats_json:
        return
    cats = json.loads(cats_json)

    logs = []
    for c in ["Audit", "RequestResponse"]:
        if any(x.get("categoryType") == "Logs" and x.get("name") == c for x in cats):
            logs.append({"category": c, "enabled": True})

    metrics = []
    for c in ["AllMetrics"]:
        if any(x.get("categoryType") == "Metrics" and x.get("name") == c for x in cats):
            metrics.append({"category": c, "enabled": True})

    if not logs and not metrics:
        return

    logs_json = json.dumps(logs, separators=(",", ":"))
    metrics_json = json.dumps(metrics, separators=(",", ":"))

    run_az(
        [
            "monitor",
            "diagnostic-settings",
            "create",
            "--name",
            diag_name,
            "--resource",
            resource_id,
            "--workspace",
            workspace_id,
            "--logs",
            logs_json,
            "--metrics",
            metrics_json,
        ],
        allow_error=True,
    )


def get_metric_sum(resource_id, metric_name, start, end, filter_expr):
    out = run_az(
        [
            "monitor",
            "metrics",
            "list",
            "--resource",
            resource_id,
            "--metric",
            metric_name,
            "--start-time",
            start,
            "--end-time",
            end,
            "--aggregation",
            "Total",
            "--interval",
            "PT1H",
            "--filter",
            filter_expr,
            "--output",
            "json",
        ],
        allow_error=True,
    )
    if not out:
        return 0
    data = json.loads(out)
    total = 0
    values = data.get("value") or []
    if not values:
        return 0
    timeseries = values[0].get("timeseries") or []
    for ts in timeseries:
        for dp in ts.get("data") or []:
            if dp.get("total") is not None:
                total += dp.get("total")
    return total


def get_deployment_metrics(resource_id, deployment_name, model_name):
    end_time = dt.datetime.utcnow()
    start_time = end_time - dt.timedelta(days=7)
    start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    metrics = {"TotalCalls": 0, "ProcessedTokens": 0, "GeneratedTokens": 0}

    for dim_name in ["DeploymentName", "ModelName"]:
        if metrics["TotalCalls"] > 0:
            break
        filter_val = deployment_name if dim_name == "DeploymentName" else model_name
        filter_expr = f"{dim_name} eq '{filter_val}'"
        for metric_name in ["Requests", "AzureOpenAIRequests"]:
            total = get_metric_sum(resource_id, metric_name, start, end, filter_expr)
            metrics["TotalCalls"] += total
            if metrics["TotalCalls"] > 0:
                break

    for dim_name in ["DeploymentName", "ModelName"]:
        if metrics["ProcessedTokens"] > 0:
            break
        filter_val = deployment_name if dim_name == "DeploymentName" else model_name
        filter_expr = f"{dim_name} eq '{filter_val}'"
        metrics["ProcessedTokens"] += get_metric_sum(
            resource_id, "ProcessedPromptTokens", start, end, filter_expr
        )

    for dim_name in ["DeploymentName", "ModelName"]:
        if metrics["GeneratedTokens"] > 0:
            break
        filter_val = deployment_name if dim_name == "DeploymentName" else model_name
        filter_expr = f"{dim_name} eq '{filter_val}'"
        metrics["GeneratedTokens"] += get_metric_sum(
            resource_id, "GeneratedTokens", start, end, filter_expr
        )

    return metrics


def parse_target_models(value):
    if not value:
        return DEFAULT_TARGET_MODELS
    if os.path.exists(value):
        with open(value, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.loads(value)


def load_retirements(path: Path = RETIREMENTS_FILE):
    if not path.exists():
        return {"foundry": [], "azure_openai": []}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "foundry": data.get("foundry", []),
        "azure_openai": data.get("azure_openai", []),
    }


def norm(val):
    return (val or "").strip().lower()


def match_retirement(model_name, model_version, retirements):
    alerts = []
    n_name = norm(model_name)
    n_ver = norm(model_version)

    for entry in retirements.get("azure_openai", []):
        if n_name == norm(entry.get("Model")) and n_ver == norm(entry.get("Version")):
            alerts.append(
                {
                    "Legacy": None,
                    "Deprecation": entry.get("Deprecation"),
                    "Retirement": entry.get("Retirement"),
                    "Replacement": entry.get("Replacement"),
                    "Source": "Azure OpenAI in Foundry Models",
                }
            )

    for entry in retirements.get("foundry", []):
        if n_name == norm(entry.get("Model")):
            alerts.append(
                {
                    "Legacy": entry.get("Legacy"),
                    "Deprecation": entry.get("Deprecation"),
                    "Retirement": entry.get("Retirement"),
                    "Replacement": entry.get("Replacement"),
                    "Source": "Foundry Models",
                }
            )

    return alerts


def main():
    parser = argparse.ArgumentParser(description="Azure OpenAI/Foundry Deployment Audit (Python)")
    parser.add_argument("--subscription-id", dest="subscription_id")
    parser.add_argument("--out-dir", dest="out_dir")
    parser.add_argument("--enable-diag", dest="enable_diag", action="store_true")
    parser.add_argument("--diag-workspace-id", dest="diag_workspace_id")
    parser.add_argument("--diag-name", dest="diag_name", default="openai-to-la")
    parser.add_argument(
        "--target-models",
        dest="target_models",
        help="JSON string or path to JSON file",
    )
    parser.add_argument(
        "--account-kinds",
        dest="account_kinds",
        default="OpenAI,AIServices",
        help="Comma-separated resource kinds to include (default: OpenAI,AIServices)",
    )

    args = parser.parse_args()

    subscription_id = args.subscription_id or get_default_subscription_id()
    out_dir = args.out_dir or f"./foundry-audit-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    target_models = parse_target_models(args.target_models)
    retirements = load_retirements()

    Path(out_dir).mkdir(parents=True, exist_ok=True)

    run_az(["account", "set", "--subscription", subscription_id])

    deploy_csv = Path(out_dir) / "openai_deployments.csv"
    detailed_logs_csv = Path(out_dir) / "log_analytics_detailed_logs.csv"
    no_diag_csv = Path(out_dir) / "openai_no_diagnostics.csv"
    targeted_csv = Path(out_dir) / "targeted_deployments.csv"
    retirements_csv = Path(out_dir) / "model_retirement_alerts.csv"

    ws_list = []

    with open(deploy_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "account",
            "resourceGroup",
            "location",
            "deployment",
            "modelName",
            "modelVersion",
            "sku",
            "capacity",
            "resourceId",
        ])

    with open(no_diag_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["resourceGroup", "account", "resourceId"])

    with open(detailed_logs_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "workspaceId",
                "TimeGenerated",
                "ResourceId",
                "Operation",
                "CallerIP",
                "Identity",
                "UserAgent",
                "Properties",
            ]
        )

    with open(targeted_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "account",
                "resourceGroup",
                "location",
                "deployment",
                "modelName",
                "modelVersion",
                "sku",
                "capacity",
                "totalCalls_7d",
                "processedTokens_7d",
                "generatedTokens_7d",
                "resourceId",
            ]
        )

    with open(retirements_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "account",
                "resourceGroup",
                "location",
                "deployment",
                "modelName",
                "modelVersion",
                "legacyDate",
                "deprecationDate",
                "retirementDate",
                "replacementModel",
                "source",
                "resourceId",
            ]
        )

    account_kinds = [k.strip() for k in (args.account_kinds or "").split(",") if k.strip()]
    if not account_kinds:
        account_kinds = ["OpenAI", "AIServices"]

    kind_filter = " || ".join([f"kind=='{k}'" for k in account_kinds])

    print(f"Discovering OpenAI/Foundry accounts in subscription {subscription_id} ...")
    accounts_json = run_az(
        [
            "resource",
            "list",
            "--subscription",
            subscription_id,
            "--resource-type",
            "Microsoft.CognitiveServices/accounts",
            "--query",
            f"[?{kind_filter}].{{name:name, rg:resourceGroup, id:id, location:location}}",
            "-o",
            "json",
        ]
    )
    accounts = json.loads(accounts_json) if accounts_json else []
    print(f"Found OpenAI accounts: {len(accounts)}")

    retirement_alerts = []

    for acc in accounts:
        name = acc.get("name")
        rg = acc.get("rg")
        rid = acc.get("id")
        loc = acc.get("location")

        print(f"Processing: {rg}/{name}")

        enable_diagnostics(rid, args.enable_diag, args.diag_workspace_id, args.diag_name)

        ds_json = run_az(
            [
                "monitor",
                "diagnostic-settings",
                "list",
                "--resource",
                rid,
                "-o",
                "json",
            ],
            allow_error=True,
        )
        ws = None
        if ds_json:
            ds = json.loads(ds_json)
            for item in ds:
                if item.get("workspaceId"):
                    ws = item.get("workspaceId")
                    break
        if ws:
            ws_list.append(ws)
        else:
            with open(no_diag_csv, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([rg, name, rid])

        deps = try_list_deployments(rid)
        if deps and deps.get("value"):
            for d in deps.get("value"):
                dep_name = d.get("name")
                model_name = (d.get("properties") or {}).get("model", {}).get("name")
                model_version = (d.get("properties") or {}).get("model", {}).get("version")
                sku = (d.get("sku") or {}).get("name")
                cap = (d.get("sku") or {}).get("capacity")

                with open(deploy_csv, "a", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerow(
                        [name, rg, loc, dep_name, model_name, model_version, sku, cap, rid]
                    )

                for alert in match_retirement(model_name, model_version, retirements):
                    retirement_alerts.append(
                        [
                            name,
                            rg,
                            loc,
                            dep_name,
                            model_name,
                            model_version,
                            alert.get("Legacy"),
                            alert.get("Deprecation"),
                            alert.get("Retirement"),
                            alert.get("Replacement"),
                            alert.get("Source"),
                            rid,
                        ]
                    )

                is_targeted = any(
                    model_name == t.get("ModelName") and model_version in t.get("Versions", [])
                    for t in target_models
                )

                if is_targeted:
                    print(
                        f"  -> Found targeted deployment: {dep_name} ({model_name} {model_version}) - fetching metrics..."
                    )
                    metrics = get_deployment_metrics(rid, dep_name, model_name)

                    total_calls = round(metrics.get("TotalCalls", 0))
                    processed_tokens = round(metrics.get("ProcessedTokens", 0))
                    generated_tokens = round(metrics.get("GeneratedTokens", 0))

                    with open(targeted_csv, "a", newline="", encoding="utf-8") as f:
                        csv.writer(f).writerow(
                            [
                                name,
                                rg,
                                loc,
                                dep_name,
                                model_name,
                                model_version,
                                sku,
                                cap,
                                total_calls,
                                processed_tokens,
                                generated_tokens,
                                rid,
                            ]
                        )

                    if total_calls > 0:
                        print(
                            f"     Usage detected: {total_calls} calls, {processed_tokens} prompt tokens, {generated_tokens} generated tokens (last 7 days)"
                        )
                    else:
                        print("     No usage detected in last 7 days")

    print(f"Saved deployments inventory: {deploy_csv}")
    print(f"Saved accounts without diagnostics: {no_diag_csv}")
    print(f"Saved targeted deployments report: {targeted_csv}")

    if retirement_alerts:
        with open(retirements_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in retirement_alerts:
                writer.writerow(row)
        print(f"Saved model retirement alerts: {retirements_csv}")
        unique_replacements = sorted(
            {
                r[9]
                for r in retirement_alerts
                if r[9] and str(r[9]).strip().lower() != "n/a"
            }
        )
        if unique_replacements:
            print("Recommended upgrades (from docs):")
            for rep in unique_replacements:
                print(f"  - {rep}")
    else:
        print("No model retirement alerts found for current deployments.")

    unique_ws = sorted(set(ws_list))
    if not unique_ws:
        print("\nNo Log Analytics workspaces found in diagnostic settings. Detailed usage report cannot be generated.")
        print("However, targeted deployments (if any) were analyzed using Azure Monitor Metrics.")
        print("Tip: run with --enable-diag --diag-workspace-id <workspaceResourceId> to enable diagnostics for detailed logs.")
        print("DONE.")
        return 0

    model_conditions = [f'Props has "{t["ModelName"]}"' for t in target_models]
    model_filter = " or ".join(model_conditions)

    versions_list = [f'"{v}"' for t in target_models for v in t.get("Versions", [])]
    versions_filter = ", ".join(versions_list)

    kql = f"""
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.COGNITIVESERVICES"
| extend Props = coalesce(
    tostring(column_ifexists("properties_s","")),
    tostring(column_ifexists("Properties_s","")),
    tostring(column_ifexists("Properties","")),
    tostring(column_ifexists("properties",""))
  )
| where {model_filter}
| where Props has_any ({versions_filter})
| extend CallerIP = tostring(column_ifexists("callerIp_s",""))
| extend Identity = tostring(column_ifexists("identity_s",""))
| extend UserAgent = tostring(column_ifexists("userAgent_s",""))
| extend Op = coalesce(tostring(column_ifexists("operation_Name","")), tostring(column_ifexists("OperationName","")))
| project TimeGenerated, ResourceId=_ResourceId, Operation=Op, CallerIP, Identity, UserAgent, Properties=Props
| order by TimeGenerated desc
| take 5000
"""

    for ws in unique_ws:
        print(f"Querying workspace: {ws}")
        res_json = run_az(
            [
                "monitor",
                "log-analytics",
                "query",
                "--workspace",
                ws,
                "--analytics-query",
                kql,
                "-o",
                "json",
            ],
            allow_error=True,
        )
        if not res_json:
            continue
        res = json.loads(res_json)
        tables = res.get("tables") or []
        if not tables:
            continue
        rows = tables[0].get("rows") or []
        if not rows:
            continue
        with open(detailed_logs_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in rows:
                if len(row) < 7:
                    continue
                writer.writerow([ws, row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

    print(f"Saved detailed logs from Log Analytics: {detailed_logs_csv}")
    print("DONE.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
