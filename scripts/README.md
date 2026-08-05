# Scripts

Thin wrappers that chain the accelerator's lifecycle steps. Each script
forwards arguments to the underlying tool — they're just for ergonomics so the
[root README](../README.md) can show a single command per phase.

| Script | Underlying tool | Phase |
|--------|-----------------|-------|
| [`run_scan.sh`](./run_scan.sh) | [`tools/discovery/Get-AzureAIDeployments.ps1`](../tools/discovery/Get-AzureAIDeployments.ps1) | Discover |
| [`run_deep_audit.sh`](./run_deep_audit.sh) | [`tools/discovery/deep-audit/`](../tools/discovery/deep-audit/) | Discover (optional deep audit) |
| [`run_audit.sh`](./run_audit.sh) | [`tools/audit/audit_codebase.py`](../tools/audit/audit_codebase.py) | Migrate |
| [`run_eval.py`](./run_eval.py) | [`tools/evaluator/cli.py`](../tools/evaluator/cli.py) | Evaluate |

```bash
# Discovery
bash scripts/run_scan.sh

# Optional deep discovery audit (diagnostics + detailed usage attribution)
bash scripts/run_deep_audit.sh --help

# Audit a target codebase
bash scripts/run_audit.sh --path /path/to/your/app

# A/B evaluation
python scripts/run_eval.py \
  --source gpt-4o --target gpt-4.1 \
  --dataset data/golden-datasets/golden_rag.sample.jsonl
```

Make the shell scripts executable with `chmod +x scripts/*.sh` after cloning.
