# Evaluator

> **Source:** Will be folded in via `git subtree` from
> [aiappsgbb/AOAI-models-migration](https://github.com/aiappsgbb/AOAI-models-migration)
> (`src/evaluate/`). The full evaluator package — `MigrationEvaluator`,
> `TestCase`, `ComparisonReport`, local SDK evaluation, Foundry cloud
> evaluation, and the `.prompty` LLM‑as‑Judge templates — is **not yet
> mirrored here**; this folder currently contains a thin **CLI shim** that the
> wrapper script `scripts/run_eval.py` calls into.
>
> See [`ATTRIBUTION.md`](../../ATTRIBUTION.md) and
> [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).

## Canonical API

```python
from src.evaluate.core import MigrationEvaluator

evaluator = MigrationEvaluator(
    source_model="gpt-4o",
    target_model="gpt-4.1",
    test_cases="data/golden-datasets/golden_rag.jsonl",
    metrics=["coherence", "fluency", "relevance", "groundedness"],
)
report = evaluator.run()
report.print_report()
```

This API is the **canonical** evaluator API for the accelerator. The CLI
shim under [`cli.py`](./cli.py) wraps it; #3's `run_evaluation.py` is
**deprecated** in favor of this CLI.

## Folder map (target state)

```
tools/evaluator/
├── cli.py                CLI entrypoint (this folder, today)
├── webui/                Flask/Streamlit visual comparator (upstream: model_migration_eval/)
└── _upstream/            ← `git subtree` of aiappsgbb/AOAI-models-migration src/evaluate/
```

## How to fold in the upstream

```bash
git remote add aoai-mig https://github.com/aiappsgbb/AOAI-models-migration.git
git subtree add --prefix=tools/evaluator/_upstream aoai-mig main --squash
# then reorganize files into the layout above in a follow-up commit
```

Until that lands, install the upstream as a sibling repo and point
`PYTHONPATH` at it, or copy `src/evaluate/` in manually.
