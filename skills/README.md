# Agent Skills

> **Status:** This folder currently contains documentation only. The skill
> definitions are consumed from upstream repos (not vendored here yet).

> **Source:** Core lifecycle skills are folded in from
> [aiappsgbb/AOAI-models-migration/.github/skills/](https://github.com/aiappsgbb/AOAI-models-migration/tree/main/.github/skills).

Use these installable agent **skills** to add migration knowledge into any
[supported coding agent](https://github.com/vercel-labs/skills#supported-agents):

| Skill | What it gives the agent | Use it when |
|-------|-------------------------|-------------|
| `aoai-model-migration` | API changes, client configuration, parameter adaptation | You are applying model-specific parameter and client updates |
| `aoai-model-lifecycle` | Retirement timelines, governance, operational checklists | You need urgency/risk framing and retirement-aware planning |
| `aoai-migration-plan` | Phased execution plans, rollout gates, rollback strategy | You are preparing pilot/canary/prod rollout plans |
| `aoai-migration-evaluation` | A/B testing, LLM‑as‑Judge, SDK & Foundry evaluation | You are validating quality/regression before or after cutover |

## What to install for this accelerator

For the best experience in this repo, install **both** skill packs:

1. Lifecycle migration skills (`aiappsgbb/AOAI-models-migration`)
2. Chat Completions → Responses API migration skill
	(`Azure-Samples/azure-openai-to-responses`)

This mirrors the repo structure:

- Lifecycle guidance in [`../docs/`](../docs/)
- Parameter/static scan in [`../tools/audit/`](../tools/audit/)
- Chat → Responses API rewrite in [`../tools/api-migration/`](../tools/api-migration/)

## Install (today — from upstream)

Prerequisites:

- Node.js + `npx`
- A supported coding agent host (Copilot, Claude Code, Codex CLI, etc.)

Install core lifecycle skills:

```bash
npx skills add aiappsgbb/AOAI-models-migration
```

Install the Chat Completions → Responses API migration skill:

```bash
npx skills add Azure-Samples/azure-openai-to-responses
```

> **Note.** The plan calls for re‑publishing these skills from this repo so
> the install string becomes `npx skills add microsoft/Foundry-Models-Accelerator`.
> That requires folding the upstream `.github/skills/` directory into this
> repo first via `git subtree` — track in a follow‑up issue.

## Tryout flow for accelerator users

Use this sequence when trying the repo end-to-end:

1. Discover + assess with docs/tools in this repo:
	- [`../tools/discovery/`](../tools/discovery/)
	- [`../docs/02-migration-paths.md`](../docs/02-migration-paths.md)
	- [`../docs/03-feasibility-assessment.md`](../docs/03-feasibility-assessment.md)
2. Run static scan:
	- [`../tools/audit/`](../tools/audit/)
3. If crossing Chat Completions → Responses API, run the API migration skill:
	- [`../tools/api-migration/`](../tools/api-migration/)
4. Validate outcomes:
	- [`../tools/evaluator/`](../tools/evaluator/)
	- [`../docs/07-evaluation-guide.md`](../docs/07-evaluation-guide.md)
5. Roll out safely:
	- [`../docs/08-execution-rollout.md`](../docs/08-execution-rollout.md)

## Prompt starters

After installation, you can ask your coding agent:

- "Use `aoai-model-migration` to map my GPT-4o parameters to GPT-5.4-mini."
- "Use `aoai-migration-plan` to generate a phased rollout with rollback gates."
- "Use `aoai-migration-evaluation` to design an A/B eval on my golden dataset."
- "Use the Azure OpenAI to Responses skill to migrate this Python app from
  `chat.completions.create(...)` to `responses.create(...)` and verify it."

These prompts align with the migration assets in this repo and reduce manual
translation work between strategy docs and code changes.

## Related — Chat Completions → Responses API skill

For the specific Chat Completions → Responses API code migration, see
[`tools/api-migration/`](../tools/api-migration/), which points at an
installable Agent Skill from
[Azure‑Samples/azure‑openai‑to‑responses](https://github.com/Azure-Samples/azure-openai-to-responses).
The skill does the scan → plan → edit → verify loop for that specific API
shape change; the four skills above cover the broader lifecycle
(model selection, retirement, plan, evaluation).
