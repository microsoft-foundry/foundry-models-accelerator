# B. Delta analysis — Source vs Target

> **Source:** Adapted from
> [saurabhvartak1982/modelmigration § B](https://github.com/saurabhvartak1982/modelmigration#b-model-delta-analysis-source-vs-target--fill-this-for-any-migration).

Create a short **delta sheet** for the source and target models. For
parameter‑level changes per target model, the canonical reference is
[`docs/05-api-changes-by-model.md`](../05-api-changes-by-model.md); this page
focuses on the *qualitative* delta you should capture in your migration plan.

## 1. Capabilities

- Instruction following / reasoning style differences
- Coding / tool‑use differences (if relevant)
- Safety behaviour differences (if relevant)

## 2. Limits

- Context window, input capacity, max output tokens
- Known limitations or special constraints (e.g., tool schema size caps,
  unsupported parameters)

## 3. Cost and rate‑limit implications

- Pricing changes (input / output token pricing; long‑context tiering if
  applicable)
- Quota, latency, and throughput differences (TPM / RPM and how you allocate
  them)

## 4. Knowledge cutoff differences

Relevant when the app relies on parametric knowledge rather than RAG.

## 5. Expected impact summary

- What could change functionally (edge cases, formatting strictness, tool
  selection, verbosity)?
- What must be retested because of the above?

---

→ Once your delta sheet is signed off, plan the actual rollout in
[**C. Deployment & rollout**](./deployment.md).
