# Attribution / Provenance Map

This file tracks where each piece of content originated so consolidated changes
can flow back upstream and so authors get credit. See
[`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md) for license text.

| Path in this repo | Upstream repo | Upstream path | Type |
|---|---|---|---|
| `docs/01-methodology/discovery.md` | [#1 modelmigration](https://github.com/saurabhvartak1982/modelmigration) | `README.md` § A | Adapted |
| `docs/01-methodology/delta.md` | #1 | `README.md` § B | Adapted |
| `docs/01-methodology/deployment.md` | #1 | `README.md` § C, E, F | Adapted |
| `docs/01-methodology/evaluation.md` | #1 | `README.md` § D | Adapted |
| `tools/discovery/Get-AzureAIDeployments.ps1` | [#2 azure-ai-deployment-scanner](https://github.com/ElisaPiccin/azure-ai-deployment-scanner) | `Get-AzureAIDeployments.ps1` | Verbatim (with added header) |
| `tools/discovery/README.md` | #2 | `README.md` | Adapted |
| `tools/audit/audit_codebase.py` | [#3 azure-openai-migration-guide](https://github.com/fatimataayeb/azure-openai-migration-guide) | `scripts/audit_codebase.py` | Verbatim (with added header) |
| `docs/05-api-changes-by-model.md` § "GPT‑4o → GPT‑5.1 quick‑switch" | #3 | `docs/api-changes.md`, `README.md` | Adapted |
| `docs/faq.md` GPT‑4o → 5.1 entries | #3 | `docs/faq.md` | Adapted |
| `docs/02-migration-paths.md` | [#4 AOAI-models-migration](https://github.com/aiappsgbb/AOAI-models-migration) | `docs/migration-paths.md` | Summarized, see upstream for full content |
| `docs/03-feasibility-assessment.md` | #4 | `docs/migration-feasibility-assessment.md` | Summarized |
| `docs/04-retirement-timeline.md` | #4 + #3 | `docs/retirement-timeline.md` | Merged single source of truth |
| `docs/06-building-golden-datasets.md` | #4 | `docs/building-golden-datasets.md` | Summarized |
| `docs/07-evaluation-guide.md` | #4 | `docs/evaluation-guide.md` | Summarized |
| `docs/08-execution-rollout.md` | #4 + #1 | `docs/migration-execution-guide.md` + #1 § C, F | Merged |
| `tools/evaluator/` | #4 | `src/evaluate/` | Pointer / stub; sync via `git subtree` |
| `tools/evaluator/webui/` | #4 | `model_migration_eval/` | Pointer / stub |
| `data/golden-datasets/` | #4 (+ templates from #3) | `data/*.jsonl`, `datasets/templates/` | Pointer + sample |
| `examples/notebooks/` | #4 | `*.ipynb` at repo root | Pointer |
| `examples/sdks/` | #4 | `docs/api-changes-by-model.md` SDK sections | Pointer |
| `skills/` | #4 | `.github/skills/` | Pointer |
| `presentation/` | #3 | `presentation/migration_deck.pptx` | Pointer |
| `tools/availability/README.md` | [#5 foundry-model-availability-notifications](https://github.com/JinLee794/foundry-model-availability-notifications) | repo root + generated site | Pointer (no source vendored — consumed via live dashboard, JSON snapshots, and GitHub issue stream) |
| `tools/api-migration/README.md` | [#6 azure-openai-to-responses](https://github.com/Azure-Samples/azure-openai-to-responses) | repo root, `migrate.py`, `skills/`, `demo/openai-chat-app-quickstart` | Pointer (no source vendored — consumed via Agent Skill, `migrate.py`, and the sample app) |
| `docs/05-api-changes-by-model.md` § "Chat Completions → Responses API" | #6 | upstream `README.md` mapping tables | Adapted (table + before/after Python example summarized) |
| `tools/discovery/deep-audit/_upstream/`, `tools/discovery/deep-audit/README.md`, `scripts/run_deep_audit.sh` | [#7 foundry_model_audit](https://github.com/anishek-microsoft/foundry_model_audit) | `README.md`, `foundry_model_audit.py`, `update_model_retirements.py`, `model_retirements.json` | Vendored via `git subtree` + wrapper + integration docs |

## Status of the merge

This repo was bootstrapped without `git clone`/`git subtree` access to the
upstreams, so larger upstream artifacts (the full evaluator Python package,
notebooks, the web UI, the PPTX, the `.gif` demos, and the JSONL datasets) are
currently represented by **README pointers** that link back to the canonical
upstream path. Once maintainership is established, fold them in with:

```bash
git subtree add --prefix=tools/evaluator/_upstream \
    https://github.com/aiappsgbb/AOAI-models-migration.git main
git subtree add --prefix=tools/discovery/_upstream \
    https://github.com/ElisaPiccin/azure-ai-deployment-scanner.git main
# …then reorganize into the final layout in a follow-up "reorg" commit.
```

That preserves `git log --follow` history and keeps the option of periodic
`git subtree pull` syncs from upstream open.
