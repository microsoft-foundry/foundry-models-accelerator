# Foundry Models Accelerator

> **Discover, assess, migrate, evaluate, and roll out Microsoft Foundry / Azure OpenAI
> model upgrades — end‑to‑end.**

> [!IMPORTANT]
> **Disclaimer.** This accelerator is **not an official Microsoft product** and is
> not supported under any Microsoft support program. It is provided **as‑is** under
> the [MIT License](./LICENSE). Always verify model availability and retirement
> dates against the
> [official Azure OpenAI Model Retirements page](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirements).

The Foundry Models Accelerator is a consolidated, lifecycle‑oriented toolkit for
teams running Microsoft Foundry / Azure OpenAI in production. It brings together
the discovery scanner, methodology playbook, evaluation framework, audit
scripts, golden datasets, and rollout guidance that previously lived in four
separate community repos — see [Attribution](#attribution) below.

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
 ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
 │ Discover │──>│  Assess  │──>│  Migrate │──>│ Evaluate │──>│ Roll out │
 └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
   deployment    target +      code diff +    A/B            rollout +
   inventory     feasibility   PR-ready       scorecard +    rollback
   (CSV)         score         changes        go/no-go       plan

          <----------- tools/availability/ (continuous) ----------->
                platform-side model & region availability signal
```

Each phase produces an artifact the next phase consumes. **You drive the
hand-offs** — the tools surface findings; you make the decisions.

### Discover — *what's deployed and what's at risk*
- **You produce:** an inventory of every Foundry / Azure OpenAI deployment in
  your tenant, enriched with retirement dates and recent usage.
- **You decide:** which deployments are in scope (still active, retiring
  soon, business-critical) and triage the rest.
- **Tools & docs:** [`tools/discovery/`](./tools/discovery) ·
  [`tools/discovery/deep-audit/`](./tools/discovery/deep-audit) (optional —
  diagnostics + per-deployment usage attribution).

### Assess — *pick a target, prove it's feasible*
- **You consume:** the in-scope deployment list from Discover.
- **You produce:** a target model per deployment plus a feasibility score
  across quality, latency, cost, compatibility, **capacity**, and **runway**.
- **You decide:** whether the target is GA in your region/SKU, whether the
  API changes are tolerable, and whether to proceed, pick a different target,
  or defer.
- **Tools & docs:** [`docs/02-migration-paths.md`](./docs/02-migration-paths.md) ·
  [`docs/03-feasibility-assessment.md`](./docs/03-feasibility-assessment.md) ·
  [`docs/04-retirement-timeline.md`](./docs/04-retirement-timeline.md) ·
  [`tools/availability/`](./tools/availability)

### Migrate — *change the code*
- **You consume:** the chosen target model + your application source.
- **You produce:** a code diff covering parameter changes for the target
  model, and — if you're crossing the Chat Completions → Responses API
  boundary — a rewritten SDK call shape. Reviewable as a normal PR.
- **You decide:** which findings to apply automatically vs. fix by hand,
  whether to introduce a thin abstraction over the SDK, and how to stage the
  diff (one PR per service, or one per model family).
- **Tools & docs:** [`tools/audit/`](./tools/audit) ·
  [`tools/api-migration/`](./tools/api-migration) ·
  [`docs/05-api-changes-by-model.md`](./docs/05-api-changes-by-model.md) ·
  [`examples/before-after/`](./examples/before-after)

### Evaluate — *prove the new model is at least as good*
- **You consume:** the migrated code + a golden dataset representative of
  your production traffic.
- **You produce:** a side-by-side scorecard (source vs. target) on quality
  metrics you defined, plus latency and cost deltas.
- **You decide:** go / no-go on the cutover — or iterate (prompt tweaks,
  param changes, different target) and re-run.
- **Tools & docs:** [`tools/evaluator/`](./tools/evaluator) ·
  [`data/golden-datasets/`](./data/golden-datasets) ·
  [`docs/06-building-golden-datasets.md`](./docs/06-building-golden-datasets.md) ·
  [`docs/07-evaluation-guide.md`](./docs/07-evaluation-guide.md)

### Roll out — *ship safely, keep a rollback path*
- **You consume:** the evaluator go-signal + the merged migration PR.
- **You produce:** a phased rollout plan (canary → % traffic → 100%) with
  explicit rollback gates and a post-cutover eval cadence.
- **You decide:** traffic percentages per phase, which metrics gate
  promotion, and the rollback trigger thresholds.
- **Tools & docs:** [`docs/01-methodology/`](./docs/01-methodology) ·
  [`docs/08-execution-rollout.md`](./docs/08-execution-rollout.md)

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

# 1. DISCOVER — inventory all model deployments in your tenant
#    (run in Azure Cloud Shell with pwsh, or locally with Azure CLI + PowerShell)
pwsh ./tools/discovery/Get-AzureAIDeployments.ps1
#    Optional deep audit for targeted model/version usage + diagnostics path:
bash scripts/run_deep_audit.sh --help

# 2. ASSESS — read the feasibility framework and pick a target
open docs/03-feasibility-assessment.md
open docs/02-migration-paths.md
#    Confirm the target is actually live in your region & SKU:
open tools/availability/README.md

# 3. AUDIT — flag code that needs parameter / API changes
python tools/audit/audit_codebase.py --path /path/to/your/app
#    If you're crossing Chat Completions → Responses API, also use the
#    API-migration scanner / Agent Skill from tools/api-migration/.
open tools/api-migration/README.md

# 4. EVALUATE — run an A/B comparison on a golden dataset
python -m pip install -r requirements.txt
cp .env_example .env   # fill in your Azure OpenAI endpoint + keys
python scripts/run_eval.py --source gpt-4o --target gpt-4.1 \
    --dataset data/golden-datasets/golden_rag.sample.jsonl

# 5. ROLL OUT — follow the phased rollout playbook
open docs/08-execution-rollout.md
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

This accelerator focuses on **text-generation model migration on Azure OpenAI /
Microsoft Foundry** (GPT‑4o family → GPT‑4.1 / GPT‑5.x / o‑series). For audio,
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
