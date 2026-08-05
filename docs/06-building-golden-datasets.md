# 06. Building Golden Datasets

> **Source:** Summarized from
> [aiappsgbb/AOAI-models-migration/docs/building-golden-datasets.md](https://github.com/aiappsgbb/AOAI-models-migration/blob/main/docs/building-golden-datasets.md).
> Per‑scenario JSONL files and template starting points live in
> [`data/golden-datasets/`](../data/golden-datasets/).

A **golden dataset** is the test fixture for every A/B model evaluation in
this accelerator. The single biggest lever for a reliable migration is having
**real production examples** in this dataset.

## Three sources, in priority order

1. **Stored Completions** (Azure OpenAI feature).
   The cheapest path — Azure already has the inputs and outputs. Export, label
   the outputs you'd like to keep producing, drop into a `.jsonl`.
2. **APIM / AI gateway logs.**
   If you front Azure OpenAI with API Management or an AI gateway, the
   request/response bodies are already logged. Sample by intent / endpoint to
   get coverage.
3. **Agent traces** (Semantic Kernel, LangChain, custom).
   For multi‑step apps, capture the *per‑step* prompts and responses so each
   step gets evaluated separately (see
   [§ Multi‑step apps](#multi-step-apps) below).

If none of these exist, **don't synthesize from the source model** — that
biases the dataset toward what the source model already does well. Have a
human author 10–30 representative prompts per intent instead.

## What to label

For each example, capture:

- `query` / `messages` — the input
- `context` — retrieved RAG docs or tool schemas, if any
- `expected` — the gold answer (human‑written)
- `must_include` / `must_not_include` — short list of substrings that must (or
  must not) appear, used as cheap deterministic checks
- `tags` — intent, difficulty, customer segment, anything you want to slice
  results by

The exact schema is in
[`data/golden-datasets/README.md`](../data/golden-datasets/README.md); it
matches the upstream `MigrationEvaluator` so you can drop files in directly.

## Sizing

| Scenario | Minimum viable | Comfortable |
|----------|----------------|-------------|
| Single‑turn Q&A | 10 | 50 |
| RAG | 10 | 50–100 (covering retrieval failures) |
| Tool / function calling | 8 | 30+ (one per tool × intent) |
| Multi‑turn | 6 | 30+ (varied conversation length) |

## Multi‑step apps

For RAG pipelines and agents, evaluate at **two layers**:

1. **End‑to‑end** — did the final answer pass quality bars?
2. **Per‑step** — did *each* step (rephrase / retrieve / generate / tool call)
   stay within its own quality bar?

E2E catches the symptom; per‑step localizes the regression. The upstream's
`samples/rag_pipeline/` walks through this end‑to‑end — see
[`docs/07-evaluation-guide.md`](./07-evaluation-guide.md).

## Maintenance

Keep the dataset versioned in git. Treat it like code: PR review for new
cases, no silent edits to expected answers (those count as a quality
*change*, not a bug fix).
