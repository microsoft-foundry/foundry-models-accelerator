# 08. Execution & Rollout

> **Source:** Merged from
> [aiappsgbb/AOAI-models-migration/docs/migration-execution-guide.md](https://github.com/aiappsgbb/AOAI-models-migration/blob/main/docs/migration-execution-guide.md)
> and #1's deployment‑strategy section
> ([`docs/01-methodology/deployment.md`](./01-methodology/deployment.md)).

The end‑to‑end **operational** playbook. Phases below are sequential.

## Phase 1 — Prepare

- [ ] Discovery complete ([`docs/01-methodology/discovery.md`](./01-methodology/discovery.md), [`tools/discovery/`](../tools/discovery/))
- [ ] Optional deep discovery audit complete for production traffic attribution and diagnostics coverage ([`tools/discovery/deep-audit/`](../tools/discovery/deep-audit/))
- [ ] Target model picked ([`docs/02-migration-paths.md`](./02-migration-paths.md))
- [ ] Target is live in your region & SKU today ([`tools/availability/`](../tools/availability/))
- [ ] Feasibility score ≥ 10 with no 0s ([`docs/03-feasibility-assessment.md`](./03-feasibility-assessment.md))
- [ ] Retirement deadline noted ([`docs/04-retirement-timeline.md`](./04-retirement-timeline.md))
- [ ] Code changes scoped via [`tools/audit/`](../tools/audit/)
- [ ] Golden dataset, expected outputs, success criteria, and evaluation
      thresholds are frozen for this migration
      ([`docs/06-building-golden-datasets.md`](./06-building-golden-datasets.md))
- [ ] Subscribed to availability‑change notifications for the target model ([`tools/availability/`](../tools/availability/)) so a regional/SKU change during rollout doesn't surprise you

## Phase 2 — Choose the deployment path, build, and pre‑deploy

- [ ] Identify the deployment type: Standard-family, PTU, or Batch.
- [ ] Choose the migration path:
  - Standard-family: configure `versionUpgradeOption`, or create a separate
    target deployment for a controlled migration.
  - PTU: choose an in-place or side-by-side migration.
  - Batch: create a side-by-side target deployment and plan to resubmit jobs.
- [ ] Confirm target-model quota when the selected path requires parallel
      deployments.
- [ ] Document the rollback or recovery path before moving traffic.
- [ ] Run the current workload unchanged against a non-production or temporary
      target deployment using the frozen dataset.
- [ ] Save the unchanged target results as the adaptation baseline.
- [ ] Record behavioral differences before changing the workload.
- [ ] Adapt prompts, parameters, tool definitions, output schemas, calling code,
      and downstream parsing as required. Use
      [`docs/05-api-changes-by-model.md`](./05-api-changes-by-model.md) for
      model-specific changes.
- [ ] Record what changed and why.
- [ ] If migrating across the Chat Completions → Responses API boundary, run the API‑migration tooling ([`tools/api-migration/`](../tools/api-migration/)) and mirror the upstream `demo/openai-chat-app-quickstart` sample as the reference shape.
- [ ] CI green on changed code (`ruff`, `pytest`, application tests).

## Phase 3 — Validate, then pilot / shadow

Before exposing users to the target:

1. Run the source model on the frozen dataset to establish the source baseline.
2. Run the adapted target on the same dataset with the same evaluators.
3. Compare quality, latency, and cost against the agreed thresholds.
4. Do not begin the pilot until all validation gates pass.

| Mode | What it does | When to use |
|------|--------------|-------------|
| **Shadow** | Mirror production traffic to the target model, **discard** the response, log + evaluate offline | After offline validation passes; detects regressions without user impact |
| **Pilot** | Real traffic, 1–5% routed to target | After offline validation and shadow results pass |

After offline validation passes, evaluate shadow outputs against the same
thresholds ([`docs/07-evaluation-guide.md`](./07-evaluation-guide.md)). Block
the pilot if any quality, latency, or cost threshold regresses.

## Phase 4 — Phased rollout

`1% → 5% → 25% → 50% → 100%`

At each step hold for at least one business cycle (e.g., 24 hours) and check:

- p95 latency vs SLO
- Error rate (429 / 5xx)
- Cost per request
- A scheduled evaluation run on a recent traffic sample
- App‑level KPIs (deflection, CSAT, conversion — whatever your app cares about)

## Phase 5 — Rollback criteria

Any **one** of these triggers the rollback or recovery action documented in
Phase 2. For side-by-side migrations, the previous deployment must still exist:

| Signal | Threshold (suggested) |
|--------|-----------------------|
| Invalid JSON / schema violations | >2× baseline |
| Tool‑call accuracy | drop >5 percentage points |
| p95 latency | breach SLO for >10 minutes |
| Token / request drift → cost | spike >25% above projection |
| 429 / 5xx error rate | >1% sustained for 10 min |
| Eval quality gate | any tracked metric regresses below threshold |

## Phase 6 — Post‑cutover

- [ ] Schedule nightly evaluation runs (see [`docs/07`](./07-evaluation-guide.md) "Continuous evaluation in CI").
- [ ] For side-by-side and Batch migrations, decommission the source deployment
      only after the rollback window closes and production remains stable.
- [ ] Update inventory (re‑run [`tools/discovery/`](../tools/discovery/)).
- [ ] Capture lessons in your runbook so the next migration is cheaper.
