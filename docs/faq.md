# FAQ

Merged from
[aiappsgbb/AOAI-models-migration](https://github.com/aiappsgbb/AOAI-models-migration#frequently-asked-questions)
and
[fatimataayeb/azure-openai-migration-guide/docs/faq.md](https://github.com/fatimataayeb/azure-openai-migration-guide/blob/master/docs/faq.md).

---

## Planning

### Do I have to migrate off GPT‑4o?

If you're on **Standard**, no — it will auto‑upgrade. But auto‑upgrade is not
the same as *being ready*. Parameters your code uses may be unsupported on
the replacement; prompts may regress silently. Plan the migration so you
control the change.

If you're on **PTU**, yes — PTU is not auto‑upgraded. See
[`docs/04-retirement-timeline.md`](./04-retirement-timeline.md).

### Which model should I target?

Read [`docs/02-migration-paths.md`](./02-migration-paths.md). Short answer:
`gpt-4.1` for the cheapest drop‑in, `gpt-5.x` when you need a quality lift,
o‑series for hard reasoning.

### How much effort per migration cycle?

With a reusable golden dataset and a config‑only model swap, each cycle is a
few hundred API calls and a code review. The investment pays off once you've
migrated more than one workload — see
[`docs/06-building-golden-datasets.md`](./06-building-golden-datasets.md).

## Code changes

### What's the absolute minimum I have to change?

Run [`tools/audit/audit_codebase.py`](../tools/audit/audit_codebase.py). At a
minimum you'll need to bump the model name, bump the `api_version`, rename
`max_tokens` → `max_completion_tokens` for GPT‑5/o‑series, and **remove**
sampling parameters (`temperature`, `top_p`, etc.) for those families. See
the matrix in [`docs/05-api-changes-by-model.md`](./05-api-changes-by-model.md).

### Should I switch `"system"` → `"developer"` in messages?

It's preferred on the GPT‑5 family. `"system"` still works but is deprecated.
The audit script flags it as MEDIUM (do it as part of the same PR).

### Do I need new datasets for every new model?

No. Mine the existing one from production (Stored Completions, APIM logs,
agent traces). See
[`docs/06-building-golden-datasets.md`](./06-building-golden-datasets.md).

## Evaluation

### Why LLM‑as‑Judge instead of similarity scoring?

Similarity (BLEU / cosine / embedding) penalizes correct answers that are
phrased differently from the gold answer, and misses hallucinations that
happen to share vocabulary. An LLM judge evaluates *meaning*. The trade‑off
is judge cost — use a strong but not the most expensive model for judging.

### How do I find *where* in a multi‑step pipeline a regression happened?

Evaluate at **two layers**: end‑to‑end and per‑step. E2E detects the
regression, per‑step localizes it. See
[`docs/07-evaluation-guide.md`](./07-evaluation-guide.md) § "Multi‑step / agent apps".

### What if a regression is detected?

Roll back to the old deployment (it should still exist — see
[`docs/08-execution-rollout.md`](./08-execution-rollout.md) Phase 2). Then
diagnose: prompt drift, missing parameter, wrong tier, or genuine quality
gap. The upstream's "remediation playbook" covers four common scenarios — see
[upstream docs](https://github.com/aiappsgbb/AOAI-models-migration/blob/main/docs/migrating-multi-step-apps.md).

## Operations

### How do I track quality over time?

Use Microsoft Foundry's named evaluation runs (built into the upstream
`MigrationEvaluator.run_foundry()`), or pipe results to Fabric + Power BI for
cross‑org reporting.

### Does this work for agentic apps (Semantic Kernel, LangChain, …)?

Yes — the model is one env variable in every framework. The code‑level
changes are the same (rename `max_tokens`, drop sampling params, etc.). See
the methodology pages under [`docs/01-methodology/`](./01-methodology/).

### How do I automate the migration at scale across many workloads?

`.env` swap + CI/CD nightly evaluator runs + a matrix strategy across target
models. The upstream ships an example
`eval-on-schedule.yml` workflow; porting it into this repo is on the
post‑consolidation enhancement list.
