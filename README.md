# Foundry Models Accelerator

> **Discover, assess, adapt, validate, roll out, and retire Microsoft Foundry /
> Azure OpenAI model upgrades — end‑to‑end.**

> [!IMPORTANT]
> **Disclaimer.** This accelerator is **not an official Microsoft product** and is
> not supported under any Microsoft support program. It is provided **as‑is** under
> the [MIT License](./LICENSE). Always verify model availability and retirement
> dates against the
> [official Azure OpenAI Model Retirements page](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirements).

The Foundry Models Accelerator is a consolidated, lifecycle‑oriented toolkit for
teams running Microsoft Foundry / Azure OpenAI in production. It follows the
six-phase [Microsoft Foundry model migration process](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/model-migration):
Discover, Assess, Adapt, Validate, Roll out, and Retire. It brings together the
discovery scanner, methodology playbook, evaluation framework, audit scripts,
golden datasets, and rollout guidance that previously lived in four separate
community repos — see [Attribution](#attribution) below.

> [!NOTE]
> **Status — not everything is mirrored locally yet.** A few components are
> currently pointers to their upstream source rather than in‑repo code: the
> [evaluator](./tools/evaluator) ships only a thin CLI shim (the full
> `MigrationEvaluator` package isn't vendored yet, so `scripts/run_eval.py`
> needs the upstream installed alongside it), and the [examples](./examples)
> (notebooks, SDK snippets, extra before/after diffs), [skills](./skills), and
> discovery [demo media](./tools/discovery/media) are folded in from upstream
> over time. Each affected folder's README states its current status.

## Who this is for

This accelerator is built for **AI developers in enterprises** who own Microsoft Foundry / Azure OpenAI deployments in
production: 

- **Enterprise platform teams** running Foundry across multiple subscriptions,
  regions, or business units (often dozens to hundreds of deployments).
- **Product teams** with a Foundry-backed product where a model
  retirement, capacity shift, or price/perf change is a release-blocking event.
- **Smaller teams with production stakes** — even a single team running
  >~5 deployments or one high-traffic `gpt-4o`-family workload that can't be
  silently swapped.

You'll get the most value if you're reacting to a concrete trigger: a
**retirement notice**, a **capacity / quota constraint**, a mandate to move off
the GPT-4o family, or an evaluation of a newer model (GPT-4.1 / GPT-5.x /
o-series) for cost or quality reasons.

## Lifecycle

```
 ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
 │ Discover │──>│  Assess  │──>│  Adapt   │──>│ Validate │──>│ Roll out │──>│  Retire  │
 └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
   signal +      target +      replay +       source/target   staged         old deployment
   inventory     feasibility   code changes   scorecard       exposure       decommissioned

       Prepare and freeze a representative test dataset before Adapt and Validate.
       <--------------- tools/availability/ (continuous) ---------------->
```

Each phase produces an artifact the next phase consumes. **You drive the
hand-offs** — the tools surface findings; you make the decisions.

### Before you migrate — *prepare a test dataset*
- **You produce:** a frozen set of representative inputs, expected outputs, and
  success criteria from production traffic, curated examples, or synthetic and
  adversarial data.
- **You decide:** which quality rubric and thresholds represent acceptable
  application behavior.
- **Why now:** Adapt needs representative inputs for replay, and Validate needs
  fixed ground truth and criteria. Changing the dataset or criteria midway
  makes source-to-target comparisons unreliable.
- **Tools & docs:** [`data/golden-datasets/`](./data/golden-datasets) ·
  [`docs/06-building-golden-datasets.md`](./docs/06-building-golden-datasets.md)

### Discover — *what's deployed and what's at risk*
- **You produce:** an inventory of every Foundry / Azure OpenAI deployment in
  your tenant, enriched with deployment type, retirement dates, suggested
  replacements, and recent usage.
- **You decide:** whether to migrate now, stay on the current model, or defer.
  For a retirement-driven migration, subtract validation and rollout time from
  the retirement date to find your real deadline.
- **Tools & docs:** [`tools/discovery/`](./tools/discovery) ·
  [`tools/discovery/deep-audit/`](./tools/discovery/deep-audit) (optional —
  diagnostics + per-deployment usage attribution).

### Assess — *pick a target, prove it's feasible*
- **You consume:** the in-scope deployment list from Discover.
- **You produce:** a target model per deployment plus a feasibility score
  across quality, latency, cost, compatibility, **capacity**, and **runway**.
- **You decide:** whether the target is available in the required region and
  deployment type, has enough quota, meets compliance requirements, and can run
  beside the source model to preserve rollback. Public benchmarks narrow the
  candidates; your workload determines the final choice.
- **Tools & docs:** [`docs/02-migration-paths.md`](./docs/02-migration-paths.md) ·
  [`docs/03-feasibility-assessment.md`](./docs/03-feasibility-assessment.md) ·
  [`docs/04-retirement-timeline.md`](./docs/04-retirement-timeline.md) ·
  [`tools/availability/`](./tools/availability)

### Adapt — *replay, diagnose, and change the workload*
- **You consume:** the chosen target model, frozen test dataset, current
  configuration, and application source.
- **You produce:** an unchanged replay baseline on the target, a record of the
  behavioral differences, and a reviewable code diff. The diff can include
  prompts, parameters, tool definitions, output schemas, response parsing, and
  SDK calls. If you're crossing the Chat Completions → Responses API boundary,
  it also includes the new call and streaming shapes.
- **You decide:** which findings to apply automatically vs. fix by hand and how
  to stage the changes. Replay the current workload unchanged before tuning so
  you can separate model-driven behavior shifts from your own adaptations.
- **Tools & docs:** [`tools/audit/`](./tools/audit) ·
  [`tools/api-migration/`](./tools/api-migration) ·
  [`docs/05-api-changes-by-model.md`](./docs/05-api-changes-by-model.md) ·
  [`examples/before-after/`](./examples/before-after)

### Validate — *prove the adapted workload is safe to ship*
- **You consume:** the adapted workload and the frozen dataset and success
  criteria prepared before migration.
- **You produce:** a source baseline and target scorecard using the same
  dataset and evaluators, covering workload-specific quality, time to first
  token and throughput, and input/output token cost per request.
- **You decide:** go / no-go on the rollout — or return to Adapt for prompt,
  parameter, schema, tool, or code changes and run validation again.
- **Tools & docs:** [`tools/evaluator/`](./tools/evaluator) ·
  [`data/golden-datasets/`](./data/golden-datasets) ·
  [`docs/06-building-golden-datasets.md`](./docs/06-building-golden-datasets.md) ·
  [`docs/07-evaluation-guide.md`](./docs/07-evaluation-guide.md)

### Roll out — *ship in stages and preserve rollback*
- **You consume:** the validation go-signal and merged adaptation PR.
- **You produce:** a phased rollout plan (non-production → canary, weighted, or
  shadow traffic → broader exposure) with explicit rollback gates, continuous
  evaluation, and production monitoring.
- **You decide:** which deployment-specific migration path to use, traffic
  percentages per phase, which metrics gate promotion, and the rollback
  thresholds. Keep the source deployment reachable until the target has proven
  itself under production load.
- **Tools & docs:** [`docs/01-methodology/`](./docs/01-methodology) ·
  [`docs/08-execution-rollout.md`](./docs/08-execution-rollout.md)

#### Migration mechanics by deployment type

| Deployment type | Migration approach |
|---|---|
| Standard, Global Standard, Data Zone Standard | Azure auto-upgrades deployments on a rolling schedule. Control timing with `versionUpgradeOption`: `OnceNewDefaultVersionAvailable`, `OnceCurrentVersionExpired`, or `NoAutoUpgrade`. Priority Processing follows the same path. |
| Provisioned (PTU) | Migrate manually, either in place (traffic moves over a 20–30 minute window without downtime) or side by side (deploy the target, test, shift traffic, then delete the source). Confirm target-model quota first. |
| Batch | Deploy the target side by side, resubmit jobs, then retire the source. Confirm target-model quota first. |

Auto-upgrade is a safety net for pay-as-you-go deployments, not a validation or
rollout plan. Provisioned and Batch deployments are not auto-upgraded. For any
deployment type, validate application behavior before the retirement date.

### Retire — *remove the old deployment and close the migration*
- **You consume:** production evidence that the target meets the rollout gates.
- **You produce:** a decommissioned source deployment, released capacity,
  archived evaluation artifacts, updated runbooks and product documentation,
  and new production traces folded into the dataset for the next migration.
- **You decide:** when the rollback window can close and which artifacts must be
  retained for governance or audit requirements.

### Stay current *(cross-phase)*
- **You produce:** alerts when a target model becomes deployable in your
  region/SKU, or when availability / retirement notices change.
- **You decide:** whether a new signal re-opens a previously-deferred
  assessment.
- **Tools & docs:** [`tools/availability/`](./tools/availability)

## Quick start

```bash
# 0. Clone
git clone https://github.com/microsoft/Foundry-Models-Accelerator.git
cd Foundry-Models-Accelerator

# 1. PREPARE — freeze representative inputs, expected outputs, and success criteria
open docs/06-building-golden-datasets.md

# 2. DISCOVER — inventory all model deployments in your tenant
#    (run in Azure Cloud Shell with pwsh, or locally with Azure CLI + PowerShell)
pwsh ./tools/discovery/Get-AzureAIDeployments.ps1
#    Optional deep audit for targeted model/version usage + diagnostics path:
bash scripts/run_deep_audit.sh --help

# 3. ASSESS — pick a target and confirm region, deployment type, quota, and cost
open docs/03-feasibility-assessment.md
open docs/02-migration-paths.md
#    Confirm the target is actually live in your region & SKU:
open tools/availability/README.md

# 4. ADAPT — replay unchanged first, then flag parameter / API changes
python tools/audit/audit_codebase.py --path /path/to/your/app
#    If you're crossing Chat Completions → Responses API, also use the
#    API-migration scanner / Agent Skill from tools/api-migration/.
open tools/api-migration/README.md

# 5. VALIDATE — compare source and target on the same frozen dataset
python -m pip install -r requirements.txt
cp .env_example .env   # fill in your Azure OpenAI endpoint + keys
python scripts/run_eval.py --source gpt-4o --target gpt-4.1 \
    --dataset data/golden-datasets/golden_rag.sample.jsonl

# 6. ROLL OUT — follow the phased rollout and rollback playbook
open docs/08-execution-rollout.md

# 7. RETIRE — after the rollback window closes, remove the source deployment,
#    archive evaluation artifacts, and update downstream documentation
```

Wrapper scripts under [`scripts/`](./scripts) chain these steps so you can run
them individually or as a pipeline.

## Repository layout

```
.
├── docs/                            # Lifecycle-organized written guidance
│   ├── 01-methodology/                Methodology backbone (from #1)
│   ├── 02-migration-paths.md          Target model selection (from #4)
│   ├── 03-feasibility-assessment.md   6-dimension feasibility framework (from #4)
│   ├── 04-retirement-timeline.md      Single source of truth for retirement dates
│   ├── 05-api-changes-by-model.md     Parameter matrix per target model
│   ├── 06-building-golden-datasets.md How to build eval data
│   ├── 07-evaluation-guide.md         Foundry & SDK evaluation patterns
│   ├── 08-execution-rollout.md        Phased rollout & rollback playbook
│   └── faq.md                         Combined FAQ
├── tools/
│   ├── discovery/                     PowerShell deployment scanner (from #2)
│   │   └── deep-audit/                Optional deep discovery audit (from #7)
│   ├── availability/                  Foundry model & region availability tracker (from #5)
│   ├── audit/                         Code-audit script (from #3) + notes
│   ├── api-migration/                 Chat Completions → Responses API migration scanner & Agent Skill (from #6)
│   └── evaluator/                     CLI evaluator + web UI placeholders (from #4)
├── data/
│   └── golden-datasets/               JSONL test cases + templates
├── examples/
│   ├── before-after/                  Per-target code diffs
│   ├── notebooks/                     Interactive walkthroughs
│   └── sdks/                          C# / JS / Java snippets
├── skills/                            Coding-agent skills package (from #4)
├── presentation/                      Customer-facing deck (from #3)
├── scripts/                           Thin wrappers (run_scan / run_audit / run_eval)
├── .github/workflows/                 CI: ruff, pytest, PSScriptAnalyzer, link check
├── LICENSE                            MIT
├── CONTRIBUTING.md
├── SECURITY.md
├── CODEOWNERS
├── THIRD_PARTY_NOTICES.md             Upstream credit per source repo
├── ATTRIBUTION.md                     Per-file provenance map
├── requirements.txt
└── .env_example
```

## Scope

This accelerator focuses on migration between **base text-generation models on
Azure OpenAI / Microsoft Foundry** (GPT‑4o family → GPT‑4.1 / GPT‑5.x /
o‑series). Fine-tuned workloads are out of scope: they aren't auto-upgraded and
require re-tuning or distillation onto a replacement base model. For audio,
image, and embedding model retirements, see the
[official retirements page](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirements);
the discovery scanner reports those deployments but the migration guidance does
not yet cover them.

## Attribution

This repository consolidates several community and Azure‑Samples projects.
Each retains the copyright of its original authors under MIT‑style terms. See
[`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md) for full notices and
[`ATTRIBUTION.md`](./ATTRIBUTION.md) for a per‑file provenance map.

| # | Source | Role here |
|---|--------|-----------|
| 1 | [saurabhvartak1982/modelmigration](https://github.com/saurabhvartak1982/modelmigration) | Methodology backbone in `docs/01-methodology/` |
| 2 | [ElisaPiccin/azure-ai-deployment-scanner](https://github.com/ElisaPiccin/azure-ai-deployment-scanner) | Discovery scanner in `tools/discovery/` |
| 3 | [fatimataayeb/azure-openai-migration-guide](https://github.com/fatimataayeb/azure-openai-migration-guide) | Audit script in `tools/audit/`, GPT‑4o→5.1 specifics in `docs/05-…`, presentation in `presentation/` |
| 4 | [aiappsgbb/AOAI-models-migration](https://github.com/aiappsgbb/AOAI-models-migration) | Evaluator, web UI, golden datasets, skills, notebooks, and most of `docs/02‑08` |
| 5 | [JinLee794/foundry-model-availability-notifications](https://github.com/JinLee794/foundry-model-availability-notifications) | Foundry model & region availability tracker pointer in `tools/availability/` |
| 6 | [Azure-Samples/azure-openai-to-responses](https://github.com/Azure-Samples/azure-openai-to-responses) | Chat Completions → Responses API migration scanner, Agent Skill, and demo app pointer in `tools/api-migration/`; mapping table folded into `docs/05-api-changes-by-model.md` |
| 7 | [anishek-microsoft/foundry_model_audit](https://github.com/anishek-microsoft/foundry_model_audit) | Optional deep discovery audit pointer and wrapper in `tools/discovery/deep-audit/` and `scripts/run_deep_audit.sh` |

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md). Security issues — please follow
[`SECURITY.md`](./SECURITY.md) rather than filing a public issue.

## License

[MIT](./LICENSE).
