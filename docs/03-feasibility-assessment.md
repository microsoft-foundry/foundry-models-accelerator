# 03. Feasibility Assessment

> **Source:** Summarized from
> [aiappsgbb/AOAI-models-migration/docs/migration-feasibility-assessment.md](https://github.com/aiappsgbb/AOAI-models-migration/blob/main/docs/migration-feasibility-assessment.md).

A migration is **feasible** when six dimensions all clear an internal bar.
Score each dimension **0 (blocker) / 1 (risky) / 2 (clear)** for each
workload. If *any* dimension is 0, fix it before migrating; if more than one
is 1, plan extra mitigation.

| # | Dimension | Question | What to do if score is 0 |
|---|-----------|----------|--------------------------|
| 1 | **Quality** | Does the target model meet the same evaluation thresholds as the source on a representative golden dataset? | Try a stronger tier (mini → full, standard → reasoning); revisit prompts |
| 2 | **Latency** | Does p95 latency stay under the SLO at expected concurrency? | Use a cheaper/faster tier; turn `reasoning_effort` down; cache / pre‑compute |
| 3 | **Cost** | Does monthly cost at projected traffic fit budget? | Pick a `*-mini` variant; shorten prompts; switch RAG retrieval to do more work upstream |
| 4 | **Compatibility** | Do supported parameters cover what the app uses today? | Refactor the calling code (run [`tools/audit/`](../tools/audit) first) |
| 5 | **Capacity** | Is the target model available with enough quota in your region & deployment type (Standard/PTU/Data Zone)? | File a quota request; consider Global / Data Zone deployment. Use [`tools/availability/`](../tools/availability/) for the live region × SKU matrix and change history. |
| 6 | **Runway** | Is the target itself not scheduled to retire soon? | Pick a newer target — see [retirement-timeline](./04-retirement-timeline.md) and the live retirement notices in [`tools/availability/`](../tools/availability/) |

## Scoring template

Copy the table below into your migration ticket for each workload:

```
Workload: <name>
Source:   gpt-4o
Target:   gpt-4.1

| Dimension       | Score (0/1/2) | Evidence / link |
|-----------------|---------------|-----------------|
| Quality         |               | eval run id …   |
| Latency         |               | load test …     |
| Cost            |               | cost model …    |
| Compatibility   |               | audit report …  |
| Capacity        |               | quota req …     |
| Runway          |               | retirement doc  |
| TOTAL (max 12)  |               |                 |
```

A workload with **TOTAL ≥ 10 and no 0s** is migration‑ready. Below 10 → keep
iterating; below 8 → consider a different target.
