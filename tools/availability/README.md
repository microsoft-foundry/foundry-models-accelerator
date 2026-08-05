# Availability — Foundry Model & Region Availability Tracker

> **Source:** Pointer to the upstream repo
> [foundry-model-availability-notifications](https://github.com/JinLee794/foundry-model-availability-notifications),
> used under MIT terms. See [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md)
> for the full notice and copyright.

> **⚠️ DISCLAIMER.** The availability tracker is **not an official Microsoft
> solution** and is not supported under any Microsoft support program. Always
> cross‑check availability against the
> [Foundry model catalog](https://ai.azure.com/explore/models) and the
> [official Foundry model retirement schedule](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule)
> before committing to a deployment plan.

This folder is the **availability‑intelligence layer** of the accelerator. The
[discovery scanner](../discovery/) tells you *what you have deployed*; the
availability tracker tells you *what you can deploy, where, as which SKU, and
how that picture has changed over time*.

It is the missing signal between **assessment** and **rollout**: even when
you've picked a target model and scored it feasible, you still need to know
that the target is live in your region under your deployment type — and that
nothing changed since you planned the cutover.

## What it produces

The upstream repo runs a scheduled GitHub Action (every ~6 hours) that:

- Fetches the current Microsoft Foundry model availability data.
- Diffs against the previous snapshot and stores both the new JSON snapshot
  and the historical diff.
- Opens a GitHub issue whenever availability changes (new model, new region,
  SKU change, retirement notice).
- Rebuilds a static website exposing:
  - Overview stats + searchable **All Models** view.
  - **Region** and **SKU‑type** views (Standard / Global / Data Zone / PTU).
  - Per‑model pages with availability matrices, deployment options, and
    retirement notices.
  - **Change history** so you can see when a model became deployable in a
    given region.

Coverage spans the Foundry catalog, not just Azure OpenAI: OpenAI chat +
o‑series, embeddings, Whisper, DALL‑E, plus Foundry families such as Phi,
Mistral, Qwen, and gpt‑oss.

## How to use it in each phase

| Phase | Question the tracker answers | Where to look |
|-------|------------------------------|---------------|
| **Assess — Migration paths** | Is the candidate target model actually deployable in my region under my preferred SKU yet? | Per‑model page → availability matrix |
| **Assess — Feasibility (#5 Capacity)** | Region × SKU coverage for the target. | Region view + SKU‑type view |
| **Assess — Feasibility (#6 Runway)** | Are retirement notices posted against the target? | Per‑model page → retirement section |
| **Retirement planning** | Live, continuously refreshed companion to the static retirement table. | Overview + change history |
| **Roll out — Phase 1 Prepare** | Has anything about the target's availability changed since I scored feasibility? | Latest snapshot + recent issues |
| **Roll out — continuous monitoring** | Subscribe to availability‑change issues as a rollout‑readiness signal. | GitHub issue stream |

The corresponding doc cross‑links:

- [`docs/02-migration-paths.md`](../../docs/02-migration-paths.md) — picking a
  target you can actually deploy.
- [`docs/03-feasibility-assessment.md`](../../docs/03-feasibility-assessment.md) —
  Capacity (#5) and Runway (#6) dimensions.
- [`docs/04-retirement-timeline.md`](../../docs/04-retirement-timeline.md) —
  live availability + retirement view alongside the static table.
- [`docs/08-execution-rollout.md`](../../docs/08-execution-rollout.md) —
  pre‑cutover readiness and post‑cutover monitoring.

## Consumption modes

There are three ways to consume the tracker; pick what fits your workflow:

1. **Browse the live website.** Quickest path for a one‑off "is X available
   in region Y today?" question. Bookmark the model page for the target you
   picked in [02‑migration‑paths](../../docs/02-migration-paths.md).
2. **Subscribe to GitHub issues.** Watch the upstream repo (or a fork) with
   *Custom → Issues* to get a notification every time availability changes.
   Treat new issues as rollout‑readiness signals — see Phase 1 of
   [08‑execution‑rollout](../../docs/08-execution-rollout.md).
3. **Pull the JSON snapshots.** The repo stores raw JSON snapshots and
   historical diffs. Use these in your own automation (e.g., a feasibility
   check that fails CI when the target you picked is no longer listed in
   your region).

## Quick start

```bash
# Option 1 — just read the dashboard
#   Open the website published by the upstream repo (see its README for the URL).

# Option 2 — fork and self-host so you control the schedule + issue stream
git clone https://github.com/JinLee794/foundry-model-availability-notifications.git
cd foundry-model-availability-notifications
# Follow the upstream README for GitHub Actions secrets + Pages setup.

# Option 3 — consume the raw JSON in your own tooling
#   See the snapshots/ folder in the upstream repo. Each entry is a point-in-time
#   snapshot; the diffs/ folder records what changed between snapshots.
```

## Why this lives next to the discovery scanner, not inside it

The [discovery scanner](../discovery/) is **tenant‑scoped** — it inventories
*your* subscriptions. The availability tracker is **platform‑scoped** — it
inventories *Azure's* offering. They answer complementary questions and have
different operational profiles (one is a one‑shot script you run; the other
is a continuously running service you subscribe to), so they live as
siblings under `tools/`.

## Attribution

- Upstream: <https://github.com/JinLee794/foundry-model-availability-notifications>
- License: MIT (see [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md) for
  the full notice, including the upstream author and copyright)

If you build on the tracker — fork it, file issues, or contribute fixes
upstream — please link back to the canonical upstream repo.
