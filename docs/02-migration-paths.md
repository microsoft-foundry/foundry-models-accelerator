# 02. Migration Paths

> **Answers one question:** *"My model is retiring — which model do I move to?"*
>
> **Authoritative source:** the
> [Foundry model retirement schedule](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule)
> is the only source of truth for retirement dates and default replacements.
> Dates below are reproduced for convenience and may drift — the
> [discovery scanner](../tools/discovery/) fetches the live table at run time.

---

## Step 1 — Know your default (what happens if you do nothing)

Standard deployments on a retiring model are **auto‑upgraded** by Azure to a
default replacement on the retirement date. You keep running, but you don't
control the change. These are the current defaults from the official schedule:

| Your model (retiring) | Retires | Auto‑upgrade lands you on | Runway of that default |
|-----------------------|---------|---------------------------|------------------------|
| `gpt-4o` (all 2024 versions) | **2026‑10‑01** | `gpt-5.1` | Good — retires 2027‑05‑15 |
| `gpt-4o-mini` | **2026‑10‑01** | `gpt-4.1-mini` | ⚠️ **Short — `gpt-4.1-mini` is already deprecated, retires 2026‑10‑14** |
| `o3-mini` | **2026‑10‑01** | `o4-mini` | ⚠️ **Short — `o4-mini` is deprecated, retires 2026‑10‑16** |
| `gpt-4.1` / `gpt-4.1-mini` / `gpt-4.1-nano` | **2026‑10‑14** | none (no default) | — must choose your own target |
| `o3` | **2026‑10‑16** | none | — must choose your own target |

**Two rules that follow from this table:**

1. **PTU deployments are never auto‑upgraded.** If you run PTU on any model
   above, you must redeploy yourself before the retirement date.
2. **Don't accept a short‑runway default.** The auto‑upgrade for `gpt-4o-mini`
   (`gpt-4.1-mini`) and `o3-mini` (`o4-mini`) both retire within two weeks of
   the model they replace. Accepting them means migrating again almost
   immediately. Choose a longer‑runway target yourself (Step 2).

---

## Step 2 — Choose your target

Pick the **cheapest model that passes your evaluation** ([07-evaluation-guide.md](./07-evaluation-guide.md))
*and* has runway into 2027. Use this by source model:

### Migrating from `gpt-4o`

| Your priority | Choose | Why |
|---------------|--------|-----|
| Quality lift, low‑latency default | **`gpt-5.1`** | GPT‑5 reasoning surface, but `reasoning_effort` defaults to `none` so it runs like a low‑latency chat model out of the box. The auto‑upgrade default and closest behavior to `gpt-4o`. **Not a byte‑for‑byte drop‑in:** remove `temperature`/`top_p`, use `max_completion_tokens` (see [05‑api‑changes](./05-api-changes-by-model.md)). Retires 2027‑05‑15. |
| Lowest cost, minimal API change | **`gpt-4.1`** ⚠️ | Cheapest, most 4o‑like surface **but it retires 2026‑10‑14, only 13 days after `gpt-4o`.** Only use as a short bridge, never as a destination. |
| Add reasoning | `gpt-5.4` or `gpt-5.5` | Reasoning models — expect higher latency and token cost. Not a drop‑in. |

### Migrating from `gpt-4o-mini`

| Your priority | Choose | Why |
|---------------|--------|-----|
| Longest runway, low‑latency | **`gpt-5-mini`** or **`gpt-5-nano`** | GPT‑5 reasoning surface but low‑latency at default effort, low cost, retires 2027‑02‑06 — far better runway than the `gpt-4.1-mini` default. |
| Match the auto‑upgrade default | `gpt-4.1-mini` ⚠️ | The official default, **but already deprecated (retires 2026‑10‑14).** Bridge only. |
| Cheapest reasoning option | `gpt-5.4-mini` ⚠️ | **Reasoning model, not a drop‑in** |

### Migrating from `o3-mini` / `o3` (reasoning workloads)

| Your priority | Choose | Why |
|---------------|--------|-----|
| Cheapest reasoning with runway | **`gpt-5.4-mini`** | Reasoning model with `reasoning_effort` control, retires 2027‑03. Longer runway than `o4-mini`. |
| Best reasoning / coding quality | **`gpt-5.5`** | Strongest reasoning, structured outputs, function calling. Retires 2027‑04‑23. |
| Match the `o3-mini` default | `o4-mini` ⚠️ | Official default but deprecated (retires 2026‑10‑16). Bridge only. |

### Vision / audio / embeddings

Stay on your current multi‑modal or embedding model until a vetted replacement
is announced on the [retirement schedule](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule).
The text‑generation guidance above does not apply to these.

---

## The one mistake to avoid: turning on heavy reasoning by accident

Every GPT‑5 model — `gpt-5.1`, `gpt-5-mini`, `gpt-5-nano`, `gpt-5.4*`,
`gpt-5.5` — is a **reasoning model** on the same unified API surface. They all:

- drop `temperature` / `top_p` (unsupported — will error),
- use `max_completion_tokens` instead of `max_tokens`,
- take `reasoning_effort` to control how much internal "thinking" happens.

What makes a GPT‑5 model feel "chat‑like" versus "heavy" is the
**`reasoning_effort` level**, not a separate model class:

- `gpt-5.1` **defaults `reasoning_effort` to `none`**, so out of the box it
  runs like a low‑latency chat model (no reasoning tokens billed) — the closest
  behavior to `gpt-4o`.
- Reasoning‑tuned variants like `gpt-5.4-mini` / `gpt-5.4-nano`, or higher
  effort levels, emit internal thinking tokens (you pay for them) and add
  latency.

The failure mode is swapping `gpt-4o-mini` → a GPT‑5 model while leaving a high
`reasoning_effort` (or picking a reasoning‑tuned variant) without reshaping the
request — it shows up as **higher p95 latency, higher token bills, and silent
prompt regressions.** For the most `gpt-4o`‑like behavior, use `gpt-5.1` /
`gpt-5-mini` / `gpt-5-nano` at `reasoning_effort=none` (or `low`).

`temperature` is unsupported on **all** GPT‑5 models — even at
`reasoning_effort=none` you must remove sampling knobs and apply the parameter
changes in [api‑changes](./05-api-changes-by-model.md).

## Sampling surface vs GPT‑5 reasoning surface at a glance

| | `gpt-4o` / `gpt-4.1` sampling surface | GPT‑5 unified reasoning surface (`gpt-5.1`, `gpt-5-mini`, `gpt-5-nano`, `gpt-5.4*`, `gpt-5.5`, o‑series) |
|--|---|---|
| Latency | Low — single forward pass | `reasoning_effort=none`/`low` → low; higher effort → higher (internal "thinking" tokens) |
| Cost | Lower per request | Depends on `reasoning_effort`; you pay for reasoning tokens when effort > `none` |
| Best for | Chat, RAG, classification, structured extraction | Same chat / RAG work at low effort; multi‑step planning, math, coding agents at higher effort |
| Parameter knobs | `temperature`, `top_p`, `max_tokens` supported | **No `temperature`/`top_p`**; `max_completion_tokens` + `reasoning_effort=none\|low\|medium\|high` |
| Drop‑in for `gpt-4o`? | ✅ `gpt-4.1` is closest (same knobs) | ⚠️ No — remove sampling knobs & use `max_completion_tokens`; `gpt-5.1` at `reasoning_effort=none` is behaviorally closest |

> **Expect a trade‑off moving `gpt-4o` → `gpt-5.x`:** cost per request is
> usually higher and latency can be slower, even at low `reasoning_effort`.
> Validate both against your SLO and budget in the
> [Feasibility Assessment](./03-feasibility-assessment.md) before committing —
> don't assume newer is cheaper.

---

## Step 3 — Confirm and commit

1. Run the [discovery scanner](../tools/discovery/) → list every deployment and
   its retirement date.
2. For each deployment, pick the **cheapest model that passes evaluation**
   ([07-evaluation-guide.md](./07-evaluation-guide.md)) and has runway into 2027.
3. Confirm the target is **deployable in your region and SKU today** — see the
   [availability tracker](../tools/availability/) for the live region × SKU
   matrix.
4. Score the migration with the
   [**Feasibility Assessment**](./03-feasibility-assessment.md) — the *Runway*
   dimension is what catches short‑runway defaults like `gpt-4.1-mini`.