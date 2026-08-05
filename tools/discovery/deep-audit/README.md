# Discovery Deep Audit (Optional)

> **Source:**
> [anishek-microsoft/foundry_model_audit](https://github.com/anishek-microsoft/foundry_model_audit)
> by Anishek Kamal, used under MIT terms.
> See [THIRD_PARTY_NOTICES.md](../../../THIRD_PARTY_NOTICES.md).

This folder adds an **optional deep discovery path** that complements the baseline
scanner in [tools/discovery/](../README.md).

Use this when you need:

- targeted model/version hunt across OpenAI + AIServices accounts
- retirement alerts per deployed model/version
- optional diagnostics auto-enable
- detailed Log Analytics usage attribution (identity, caller IP, user agent)

Use the baseline scanner when you need:

- fast tenant-wide inventory
- retirement + token metrics with minimal moving parts
- no diagnostics mutation

## Why this is separate

The baseline discovery scanner is the default lifecycle entrypoint and remains
authoritative for day-to-day inventory. Deep audit is a heavier workflow with
optional diagnostic-settings mutation and potentially sensitive detailed logs,
so it is intentionally isolated.

## Upstream source and sync

Deep audit is vendored from upstream as a subtree under:
`tools/discovery/deep-audit/_upstream/`

Initial vendor command:

```bash
git remote add foundry-model-audit https://github.com/anishek-microsoft/foundry_model_audit.git
git subtree add --prefix=tools/discovery/deep-audit/_upstream foundry-model-audit main --squash
```

Update command:

```bash
git subtree pull --prefix=tools/discovery/deep-audit/_upstream foundry-model-audit main --squash
```

## Run

From repository root:

```bash
bash scripts/run_deep_audit.sh --help

# Example: enable diagnostics and write reports to a timestamped folder
bash scripts/run_deep_audit.sh --enable-diag --diag-workspace-id "/subscriptions/.../resourceGroups/.../providers/Microsoft.OperationalInsights/workspaces/..."
```

## Validation matrix (tested)

Environment: Windows, PowerShell terminal, bash available.

| Command | Status | Observed result |
|---|---|---|
| `bash scripts/run_deep_audit.sh --help` | PASS | Wrapper executed vendored `_upstream/foundry_model_audit.py` and printed argparse help with expected flags. |

Notes:

- A first run failed due CRLF line endings in `scripts/run_deep_audit.sh`.
- The wrapper was normalized to LF and then validated successfully.
- Full end-to-end audit run was not executed here because it requires live Azure context (`az login`, permissions, and optionally Log Analytics workspace IDs).

## Expected outputs

The upstream script emits CSV artifacts similar to:

- `openai_deployments.csv`
- `targeted_deployments.csv`
- `openai_no_diagnostics.csv`
- `log_analytics_detailed_logs.csv`
- `model_retirement_alerts.csv`

## Security note

Deep audit artifacts can contain sensitive telemetry fields (for example IP,
identity, and user agent). Do not commit generated output folders.
