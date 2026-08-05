# 07. Evaluation Guide

> **Source:** Summarized from
> [aiappsgbb/AOAI-models-migration/docs/evaluation-guide.md](https://github.com/aiappsgbb/AOAI-models-migration/blob/main/docs/evaluation-guide.md)
> and #3's evaluation guide. See also the methodology page
> [`docs/01-methodology/evaluation.md`](./01-methodology/evaluation.md) for
> the *why*; this page is the *how*.

## Three ways to evaluate

| Mode | When to use | Tooling |
|------|-------------|---------|
| **Local CLI** | Inner loop, quick A/B during code change | [`tools/evaluator/cli.py`](../tools/evaluator/cli.py), `scripts/run_eval.py` |
| **Visual web UI** | Stakeholder review, side‑by‑side reading of individual cases | [`tools/evaluator/webui/`](../tools/evaluator/webui/) |
| **Microsoft Foundry cloud eval** | Track quality over time, share across teams, gate releases | `MigrationEvaluator.run_foundry(...)`, see upstream `src/evaluate/foundry.py` |

All three modes share the **same dataset schema** (see
[`docs/06`](./06-building-golden-datasets.md)) and the same metrics.

## Core metrics

| Metric | Range | What it answers |
|--------|-------|-----------------|
| `coherence` | 1–5 | Does the answer make sense as a piece of writing? |
| `fluency` | 1–5 | Is the language natural? |
| `relevance` | 1–5 | Does the answer address the user's question? |
| `groundedness` | 1–5 (RAG only) | Is every claim supported by the provided context? |
| `similarity` | 0–1 | How close to the labeled gold answer? (Useful but flawed — see FAQ.) |
| `tool_call_accuracy` | 0–1 | Did the model call the right tool with the right args? |

Default judges are **LLM‑as‑Judge** using a strong target model (e.g.,
`gpt-4.1` or `gpt-5.5`). Configure the judge deployment via
`AZURE_OPENAI_JUDGE_DEPLOYMENT` in [`.env`](../.env_example).

## A typical run

```bash
python scripts/run_eval.py \
  --source gpt-4o \
  --target gpt-4.1 \
  --dataset data/golden-datasets/golden_rag.sample.jsonl \
  --metrics coherence fluency relevance groundedness
```

Output is a side‑by‑side report: per‑case scores for source vs target, plus
aggregate deltas. Set a quality gate (e.g., **no metric regresses by more
than 0.2 points on average, and no case regresses by more than 1 point**) and
fail the rollout if it doesn't pass — wire this into
[`docs/08-execution-rollout.md`](./08-execution-rollout.md).

## Multi‑step / agent apps

Run **two evaluations**:

1. End‑to‑end (single dataset, judge the final answer).
2. Per‑step (one dataset per step, judge each step's I/O against its own
   expectation).

E2E detects regressions; per‑step localizes them.

## Continuous evaluation in CI

A nightly GitHub Action that runs the evaluator on the same dataset against
production traffic is the cheapest way to detect drift — see the upstream
`.github/workflows/eval-on-schedule.yml` for a template. Follow‑up issue: port
it into this repo once the evaluator is folded in.
