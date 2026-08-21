# C. Deployment & rollout

> **Source:** Adapted from
> [saurabhvartak1982/modelmigration § C, E, F](https://github.com/saurabhvartak1982/modelmigration).
> See also [`docs/08-execution-rollout.md`](../08-execution-rollout.md) for the
> tooling‑heavy operational view.

## Deployment strategy

The supported migration path depends on the deployment type:

| Deployment type | Supported migration path |
|-----------------|--------------------------|
| Standard, Global Standard, Data Zone Standard | Azure auto-upgrades deployments on a rolling schedule. Control timing with `versionUpgradeOption`. You can still create a separate target deployment for controlled testing and rollback. |
| Provisioned (PTU) | Choose an in-place migration, which moves traffic over 20–30 minutes without downtime, or a side-by-side migration. Confirm target-model quota before deploying side by side. |
| Batch | Deploy the target side by side, resubmit jobs, and retire the source deployment. |

Prefer side-by-side migration when risk, validation requirements, or rollback
needs justify the additional quota. Keep the source deployment available until
the target passes production rollout gates.

For parallel testing, ensure quota headroom or plan a PTU capacity split. If the
target deployment will also serve as the judge model for AI-assisted
evaluations, plan evaluation runs for off-peak hours.

## Performance and cost validation

- Load test with realistic concurrency and prompt sizes.
- Track p50 / p95 latency, error rate, retries, and timeouts.
- Track cost drivers: token / request drift and any long‑context usage
  patterns.

## Production rollout

### 1. Traffic shifting mechanism

- In‑app routing (percentage or stable hashing)
- APIM weighted routing
- Mesh / canary at the service layer

### 2. Rollout plan

`1% → 5% → 25% → 50% → 100%` with **hold points** tied to metrics / evals.

### 3. Post‑cutover continuous evaluation

Periodically re‑run Foundry evaluations to detect drift / regression.

### 4. Rollback conditions

- Invalid JSON spike
- Tool‑call accuracy drop
- p95 latency breach
- Token / request or cost spike
- Elevated error rates (429 / 5xx)

---

→ For the testing harness that backs every gate above, see
[**D. Evaluation & testing**](./evaluation.md).
