#!/usr/bin/env python
import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

DEFAULT_FILE = Path(__file__).with_name("model_retirements.json")

FOUNDRY_FIELDS = ["Model", "Legacy", "Deprecation", "Retirement", "Replacement"]
AOAI_FIELDS = ["Model", "Version", "Deprecation", "Retirement", "Replacement"]


def _clean(value):
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text.lower() == "null":
        return None
    return text


def _load_csv(path: Path, fields):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in fields if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"Missing columns in {path}: {', '.join(missing)}")
        rows = []
        for row in reader:
            item = {k: _clean(row.get(k)) for k in fields}
            if item.get("Model"):
                rows.append(item)
        return rows


def _load_json_list(path: Path, fields):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"JSON file must contain a list: {path}")
    rows = []
    for row in data:
        item = {k: _clean(row.get(k)) for k in fields}
        if item.get("Model"):
            rows.append(item)
    return rows


def _load_existing(path: Path):
    if not path.exists():
        return {
            "last_updated_utc": None,
            "sources": {
                "foundry": "https://learn.microsoft.com/azure/ai-foundry/concepts/model-lifecycle-retirement?view=foundry-classic",
                "azure_openai": "https://learn.microsoft.com/azure/ai-foundry/openai/concepts/model-retirements?view=foundry-classic&tabs=text",
            },
            "foundry": [],
            "azure_openai": [],
        }
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Update model_retirements.json from CSV or JSON inputs"
    )
    parser.add_argument(
        "--file",
        dest="file",
        default=str(DEFAULT_FILE),
        help="Path to model_retirements.json",
    )
    parser.add_argument("--foundry-csv", dest="foundry_csv")
    parser.add_argument("--foundry-json", dest="foundry_json")
    parser.add_argument("--azure-openai-csv", dest="aoai_csv")
    parser.add_argument("--azure-openai-json", dest="aoai_json")

    args = parser.parse_args()

    if not any([args.foundry_csv, args.foundry_json, args.aoai_csv, args.aoai_json]):
        print("Provide at least one input: --foundry-csv/json or --azure-openai-csv/json")
        return 2

    path = Path(args.file)
    data = _load_existing(path)

    if args.foundry_csv:
        data["foundry"] = _load_csv(Path(args.foundry_csv), FOUNDRY_FIELDS)
    if args.foundry_json:
        data["foundry"] = _load_json_list(Path(args.foundry_json), FOUNDRY_FIELDS)

    if args.aoai_csv:
        data["azure_openai"] = _load_csv(Path(args.aoai_csv), AOAI_FIELDS)
    if args.aoai_json:
        data["azure_openai"] = _load_json_list(Path(args.aoai_json), AOAI_FIELDS)

    data["last_updated_utc"] = dt.datetime.utcnow().strftime("%Y-%m-%d")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"Updated {path}")
    print(f"Foundry models: {len(data.get('foundry', []))}")
    print(f"Azure OpenAI models: {len(data.get('azure_openai', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
