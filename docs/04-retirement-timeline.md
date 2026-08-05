# 04. Retirement Timeline

> **Authoritative source:** The
> [Foundry model retirement schedule](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule)
> is the **only** authoritative source for retirement dates and default
> replacements. Dates here are reproduced for convenience and **may drift**;
> the [`tools/discovery/`](../tools/discovery) scanner fetches the live table
> at run time, so its output is always current.

This page is the **single source of truth** within this repo (merged from
sources #3 and #4). When in doubt, run the scanner.

## Text‑generation models

This table answers *"when does it retire, and what's the auto‑upgrade default?"*
For **which target to actually pick** (and why the defaults below are often the
wrong destination), see [02-migration-paths](./02-migration-paths.md).

| Model (retiring) | Retires | Auto‑upgrade default (Standard only) | Notes |
|------------------|---------|--------------------------------------|-------|
| `gpt-4o` (all 2024 versions) | **2026‑10‑01** | `gpt-5.1` | Low‑latency at the default `reasoning_effort=none`, good runway (retires 2027‑05‑15). The `gpt-4o` `2024-08-06-ev3` version already retired 2026‑03‑31. |
| `gpt-4o-mini` | **2026‑10‑01** | `gpt-4.1-mini` ⚠️ | Default is **already deprecated** (retires 2026‑10‑14). Prefer `gpt-5-mini` / `gpt-5-nano` instead. |
| `o3-mini` | **2026‑10‑01** | `o4-mini` ⚠️ | Default is **deprecated** (retires 2026‑10‑16). Prefer `gpt-5.4-mini`. |
| `gpt-4.1` / `gpt-4.1-mini` / `gpt-4.1-nano` | **2026‑10‑14** | none | No default — choose your own target. Do **not** use `gpt-4.1` as a migration destination. |
| `o3` | **2026‑10‑16** | none | No default — choose your own target. |
| `o4-mini` | **2026‑10‑16** | none | Deprecated — no default. |
| `gpt-4-turbo` / `gpt-4` | Already retired | — | Migrate to `gpt-5.1`. |

> ⚠️ **The auto‑upgrade default is not always a safe destination.** For
> `gpt-4o-mini` and `o3-mini`, the default replacement is itself deprecated and
> retires within ~2 weeks of the model it replaces. Accepting it means
> migrating again almost immediately — pick a longer‑runway target from
> [02-migration-paths](./02-migration-paths.md).

## What auto‑upgrade means

**Standard** deployments are upgraded automatically by Azure starting on the
auto‑upgrade date and **continue to function** with the replacement model.
This is good for safety nets, **not** good for change control:

- Prompts that depended on quirks of the old model may regress silently.
- Parameters unsupported by the new model become errors.
- Cost characteristics change.

**PTU** deployments are **not** auto‑upgraded — you must redeploy. Plan ahead.

## Urgency rules

| If your deployment is… | Action |
|------------------------|--------|
| **PTU** on a retiring model | **Highest priority.** No auto‑upgrade. Run the discovery scanner and start the migration **at least 90 days** before the retirement date. |
| **Standard** on a retiring model, in production | High priority. Plan to migrate before auto‑upgrade so you control the change. |
| **Standard** in dev / test | Medium. Use the auto‑upgrade window to learn what changes. |
| Not retiring soon | Still worth migrating opportunistically for cost / quality wins (see [02-migration-paths](./02-migration-paths.md)). |

## How to keep this page accurate

CI runs the upstream Microsoft Docs URL through a markdown link checker; a
follow‑up enhancement (see the plan) is to auto‑refresh the table on a
schedule by parsing the same upstream that the discovery scanner reads. Until
then, **trust the scanner output and the official page over this table**.

For a continuously refreshed companion view — per‑model availability matrices,
region/SKU change history, and retirement notices surfaced as GitHub issues —
see [`tools/availability/`](../tools/availability/). The static table here
answers *"when does it retire?"*; the tracker answers *"and is the
replacement deployable in my region yet?"*.
