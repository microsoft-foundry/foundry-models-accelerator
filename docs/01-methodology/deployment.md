# C. Deployment & rollout

> **Source:** Adapted from
> [saurabhvartak1982/modelmigration § C, E, F](https://github.com/saurabhvartak1982/modelmigration).
> See also [`docs/08-execution-rollout.md`](../08-execution-rollout.md) for the
> tooling‑heavy operational view.

## Deployment strategy

1. **Create a new deployment** for the target model — do **not** replace the
   existing one in place.
2. Ensure quota allocation supports parallel testing:
   - If using **PTU**, plan a capacity split.
   - If using **Standard**, ensure quota headroom.
   - If the same target deployment will also be the **judge model** for
     AI‑assisted evaluations, plan eval runs for off‑peak hours.
3. **Keep rollback easy:** don't delete the old deployment until cutover is
   stable.

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
