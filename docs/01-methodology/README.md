# Methodology

> **Source:** Adapted from [saurabhvartak1982/modelmigration](https://github.com/saurabhvartak1982/modelmigration)
> by Saurabh Vartak, with acknowledgement to Prafulla (`@prwani`). Used under MIT
> terms — see [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).

This is the **narrative backbone** of the accelerator. Everything in the rest
of `docs/` and the tools under `tools/` operationalizes one of the four phases
below.

| Phase | Question it answers | File |
|-------|---------------------|------|
| **A. Discovery** | What does the app do today, and how does it use the model? | [`discovery.md`](./discovery.md) |
| **B. Delta analysis** | What changes when we swap source → target? | [`delta.md`](./delta.md) |
| **C. Deployment & rollout** | How do we ship the change safely? | [`deployment.md`](./deployment.md) |
| **D. Evaluation & testing** | How do we know the new model is at least as good? | [`evaluation.md`](./evaluation.md) |

The phases are intentionally model‑agnostic. For target‑model‑specific
information (parameter changes, retirement dates, etc.), see
[`docs/02-migration-paths.md`](../02-migration-paths.md) and
[`docs/05-api-changes-by-model.md`](../05-api-changes-by-model.md).
