# D. Evaluation & testing

> **Source:** Adapted from
> [saurabhvartak1982/modelmigration § D](https://github.com/saurabhvartak1982/modelmigration#d-evaluation--testing-make-it-repeatable).
> For the tooling and concrete metrics, see
> [`docs/07-evaluation-guide.md`](../07-evaluation-guide.md) and
> [`tools/evaluator/`](../../tools/evaluator).

Make evaluation **repeatable**. Split into two layers.

## D1. Functional testing (humans + automated assertions)

- Functional correctness (workflow‑specific, including edge cases)
- Schema correctness (JSON validity, required fields, enum values, parsing
  robustness)
- Tool / function‑calling correctness (tool selection + parameter correctness)
- Token / request drift (input and output token changes)
- Safety behaviour where relevant

## D2. Foundry evaluations as regression gates (automated + scalable)

Use evaluations as a repeatable **quality gate** alongside functional testing:

- For Q&A / RAG: `QAEvaluator` (Relevance, Groundedness, Fluency, Coherence,
  Similarity, F1)
- For agents / tools: `ToolCallAccuracyEvaluator` (relevance, parameter
  correctness, etc.)
- Run evaluations locally and track in Foundry via the Azure AI Evaluation SDK
  workflow.
- Treat eval runs as **comparable baselines** (source vs target) and define
  thresholds.

### Golden dataset guidance

Label expected behaviours explicitly. Examples:

- "must call tool X"
- "must not hallucinate beyond retrieved context"
- "must return schema‑valid JSON"
- "must refuse / safe‑complete"

See [`docs/06-building-golden-datasets.md`](../06-building-golden-datasets.md)
for how to build these datasets from production traffic.

## Model‑specific notes

If the target model has known issues (e.g., tool schema size limits), add
targeted tests. Track these in
[`docs/05-api-changes-by-model.md`](../05-api-changes-by-model.md).

## Observability

Observability (including Evaluations) is part of **GenAIOps**; use it during
test *and* after release.
