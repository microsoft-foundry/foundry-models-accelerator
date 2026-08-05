# Golden Datasets

> **Source:** Datasets live upstream at
> [`aiappsgbb/AOAI-models-migration/data/`](https://github.com/aiappsgbb/AOAI-models-migration/tree/main/data);
> templates come from
> [`fatimataayeb/azure-openai-migration-guide/datasets/templates/`](https://github.com/fatimataayeb/azure-openai-migration-guide/tree/master/datasets/templates).
> A small sample is included here so the wrapper scripts and the evaluator CLI
> work out of the box.

Golden datasets are the **A/B test ground truth** for a migration. Each line of
a `.jsonl` file is one test case.

## Scenarios (upstream)

| Scenario | File (upstream) | Count | What it covers |
|----------|-----------------|-------|----------------|
| RAG / grounded Q&A | `golden_rag.jsonl` | 10 | Did the answer use the retrieved context faithfully? |
| Classification | `golden_classification.jsonl` | 10 | Intent and sentiment |
| Tool / function calling | `golden_tool_calling.jsonl` | 8 | Did the right tool get called with the right args? |
| Translation | `golden_translation.jsonl` | 6 | EN → IT / DE / ES |
| Summarization | `golden_summarization.jsonl` | 6 | Meeting notes, emails, incidents |
| Agent multi‑step | `golden_agent.jsonl` | 8 | Multi‑step reasoning |
| Multi‑turn | `golden_multiturn.jsonl` | 6 | Context preservation across turns |

Fold the full datasets in via `git subtree` (see [`ATTRIBUTION.md`](../../ATTRIBUTION.md)).

## What ships in this repo today

- [`golden_rag.sample.jsonl`](./golden_rag.sample.jsonl) — 3 RAG cases, enough
  to smoke‑test the evaluator CLI.
- [`templates/`](./templates) — empty‑schema templates from #3 for the
  scenarios you don't yet have data for.

## Schema

Each line is a JSON object. Field names match the upstream evaluator
(`MigrationEvaluator`) so files are drop‑in compatible:

```jsonc
{
  "id": "rag-001",
  "query": "What is Microsoft Foundry?",
  "context": "Microsoft Foundry is the unified platform for building, …",
  "expected": "It's the unified platform for building generative-AI apps on Azure.",
  "must_include": ["unified platform"],
  "must_not_include": []
}
```

See [`docs/06-building-golden-datasets.md`](../../docs/06-building-golden-datasets.md)
for how to **build** one of these from production traffic, APIM logs, or
stored completions.
