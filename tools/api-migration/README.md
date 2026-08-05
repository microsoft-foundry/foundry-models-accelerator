# API Migration — Chat Completions → Responses API

> **Source:** Pointer to the upstream repo
> [Azure-Samples/azure-openai-to-responses](https://github.com/Azure-Samples/azure-openai-to-responses),
> used under MIT terms. See [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md)
> for the full notice and copyright.

> **⚠️ DISCLAIMER.** This is an Azure‑Samples repo — provided **as‑is** for
> illustrative purposes and **not supported** under any Microsoft support
> program. Always verify the produced changes against the
> [official OpenAI Responses API documentation](https://platform.openai.com/docs/api-reference/responses)
> and your application's own tests before shipping.

This folder is the **API‑migration layer** of the accelerator. The
[discovery scanner](../discovery/) tells you *what you've deployed*; the
[code audit](../audit/) tells you *which parameters won't work on the new
model*; this layer tells you *how to rewrite the SDK calls themselves* when
the migration crosses the Chat Completions → Responses API boundary.

It is the canonical execution asset for the "API migration" step in
[`docs/05-api-changes-by-model.md`](../../docs/05-api-changes-by-model.md):
GPT‑5.x and newer models require the Responses API, and the upstream repo
translates that requirement into precise, file‑level code changes teams can
apply and verify.

## What it produces

The upstream repo ships four complementary assets:

| Asset | What it does | Where it lives upstream |
|-------|--------------|-------------------------|
| **Agent Skill** | Installable skill for GitHub Copilot and other coding agents. Scans the codebase, plans edits, migrates files, and runs verification — interactively. | `skills/` in the upstream repo |
| **`migrate.py` scanner** | Standalone Python scanner that flags Chat Completions usage and proposes Responses API replacements. Sibling in spirit to [`tools/audit/`](../audit/). | `migrate.py` at upstream root |
| **Fully‑migrated demo app** | End‑to‑end "before / after" Python sample showing the entire shape change (client, request, response, frontend). | `demo/openai-chat-app-quickstart` |
| **Reference documentation** | API support matrix by model + region, known limitations for older models, special handling for reasoning / o‑series parameters, framework‑specific guidance, and frontend guidance. | Upstream README |

## How it fits the lifecycle

| Phase | Question this layer answers | Where to look |
|-------|------------------------------|---------------|
| **Migrate — API surface** | What changes when I move from `AzureOpenAI` + Chat Completions to OpenAI client + Responses API? | Upstream README mapping tables; [`docs/05-api-changes-by-model.md`](../../docs/05-api-changes-by-model.md) § *Chat Completions → Responses API* |
| **Migrate — code edits** | Where in *my* codebase do I need to edit, and what should each edit look like? | Agent Skill (interactive) or `migrate.py` (batch) |
| **Migrate — verification** | Did I migrate correctly end‑to‑end? | Upstream `demo/openai-chat-app-quickstart` as the reference shape + the skill's verification step |
| **Migrate — model compatibility** | Does the target model actually support the Responses API in my region? | Upstream support matrix; cross‑check with [`tools/availability/`](../availability/) |
| **Roll out — Phase 2 Build** | Have I applied all the SDK / wire‑format changes the new endpoint requires? | Agent Skill verification + `tools/audit/` for residual parameter issues |

## Mapping at a glance

The full canonical mapping lives in
[`docs/05-api-changes-by-model.md`](../../docs/05-api-changes-by-model.md) §
*Chat Completions → Responses API*. The headline changes:

| Concern | Before (Chat Completions) | After (Responses API) |
|---------|---------------------------|-----------------------|
| Client | `AzureOpenAI(...)` | `OpenAI(base_url=".../openai/v1/", ...)` |
| Endpoint | `…/openai/deployments/{name}/chat/completions?api-version=…` | `…/openai/v1/responses` (no `api-version`) |
| Call | `client.chat.completions.create(...)` | `client.responses.create(...)` |
| Input field | `messages=[{"role": …, "content": …}]` | `input=…` |
| Output access | `resp.choices[0].message.content` | `resp.output_text` |
| Reasoning models | n/a | `reasoning={"effort": "low\|medium\|high"}` |

## Consumption modes

Pick what fits your workflow:

1. **Run the Agent Skill** (recommended for most teams). Install the upstream
   skill in your coding agent, point it at your repo, and let it do the
   per‑file scan → plan → edit → verify loop interactively. This is the
   highest‑leverage path because the model can reason about call sites the
   regex scanners cannot.
2. **Run `migrate.py` as a batch scanner.** Useful when you want a CI‑gateable
   diff or a non‑interactive report. Complements [`tools/audit/`](../audit/),
   which catches parameter‑level problems on the *Chat Completions* side
   *before* you do the Responses migration.
3. **Read the migrated demo app.** When the skill is ambiguous on a specific
   call shape (streaming, structured outputs, tools), open
   `demo/openai-chat-app-quickstart` in the upstream repo and mirror its
   pattern.

## Quick start

```bash
# Option 1 — install the Agent Skill (interactive)
#   Follow the upstream README for the exact install string for your coding
#   agent. The skill will scan, plan, migrate, and verify.

# Option 2 — clone and run the standalone scanner
git clone https://github.com/Azure-Samples/azure-openai-to-responses.git
cd azure-openai-to-responses
python migrate.py --path /path/to/your/app

# Option 3 — read the fully-migrated sample app
#   See demo/openai-chat-app-quickstart in the cloned repo.
```

## Recommended sequence with the rest of the accelerator

```
1. tools/discovery/      — what do I have deployed?
2. docs/02 + docs/03     — pick a target, score feasibility
3. tools/availability/   — confirm target is live in my region/SKU
4. tools/audit/          — flag Chat Completions parameters that won't work
5. tools/api-migration/  — rewrite the SDK calls themselves (this folder)
6. tools/evaluator/      — A/B the migrated code against the old deployment
7. docs/08               — phased rollout
```

Steps 4 and 5 are sequential but tight: `tools/audit/` finds the
parameter‑level issues that block the new model; `tools/api-migration/`
rewrites the call shape that the new endpoint requires. Most real migrations
need both.

## Why this lives next to (not inside) `tools/audit/`

`tools/audit/` is a **regex‑level static scanner** with a narrow, well‑defined
job: flag known‑bad parameter names. It's intentionally simple and easy to
wire into CI.

`tools/api-migration/` is a **structural code‑transformation layer** that
needs to reason about call sites, control flow, and the surrounding
framework. Its primary delivery vehicle is an LLM‑driven Agent Skill, not a
regex. Different operational profile, different consumption mode — sibling,
not nested.

## Attribution

- Upstream: <https://github.com/Azure-Samples/azure-openai-to-responses>
- License: MIT (see [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md)
  for the full notice and copyright)

If you build on the upstream repo — fork it, file issues, or contribute fixes
— please link back to the canonical upstream repo.
