# Methodology

> **Source:** Adapted from [saurabhvartak1982/modelmigration](https://github.com/saurabhvartak1982/modelmigration)
> by Saurabh Vartak, with acknowledgement to Prafulla (`@prwani`). Used under MIT
> terms — see [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).

This is the **narrative backbone** of the accelerator. It preserves the four-part
methodology developed by Saurabh Vartak from field experience. Everything in the
rest of `docs/` and the tools under `tools/` operationalizes one or more of
these workstreams.

| Workstream | Question it answers | File |
|------------|---------------------|------|
| **A. Discovery** | What does the app do today, and how does it use the model? | [`discovery.md`](./discovery.md) |
| **B. Delta analysis** | What changes when we swap source → target? | [`delta.md`](./delta.md) |
| **C. Deployment & rollout** | How do we ship the change safely? | [`deployment.md`](./deployment.md) |
| **D. Evaluation & testing** | How do we know the new model is at least as good? | [`evaluation.md`](./evaluation.md) |

## How this maps to the Microsoft Foundry migration process

The A–D labels preserve the source methodology; they are **not a chronological
execution order**. For an end-to-end migration, follow the six-phase
[Microsoft Foundry model migration process](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/model-migration):
**Discover → Assess → Adapt → Validate → Roll out → Retire**. Prepare and freeze
the test dataset before Adapt and Validate.

| Field methodology workstream | Foundry lifecycle phases |
|------------------------------|--------------------------|
| **A. Discovery** | Prepare, Discover, and part of Assess |
| **B. Delta analysis** | Assess and Adapt |
| **D. Evaluation & testing** | Validate, plus continuous evaluation during Roll out |
| **C. Deployment & rollout** | Roll out and Retire |

In execution, **D. Evaluation & testing gates C. Deployment & rollout**. The
evaluation workstream also continues after deployment to detect production
regressions.

The workstreams are intentionally model‑agnostic. For target‑model‑specific
information (parameter changes, retirement dates, etc.), see
[`docs/02-migration-paths.md`](../02-migration-paths.md) and
[`docs/05-api-changes-by-model.md`](../05-api-changes-by-model.md).
