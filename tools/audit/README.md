# Audit — Codebase scan for migration patterns

> **Source:** From
> [fatimataayeb/azure-openai-migration-guide/scripts/audit_codebase.py](https://github.com/fatimataayeb/azure-openai-migration-guide/blob/master/scripts/audit_codebase.py)
> by [Fatima Taayeb](https://github.com/fatimataayeb), used under MIT terms.
> See [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).

A simple regex‑based scanner that flags **code patterns** that won't work (or
will silently degrade) after migrating off GPT‑4o. Complementary to the
runtime [`tools/evaluator/`](../evaluator/): this one finds *where* you need
to change code; the evaluator tells you whether the change preserved quality.

## What it flags

| Issue | Severity | Why |
|-------|----------|-----|
| `temperature=…`, `top_p=…`, `frequency_penalty=…`, `presence_penalty=…`, `logprobs=…` | HIGH | Unsupported on GPT‑5.x / o‑series — will error |
| `max_tokens=…` | HIGH | Renamed to `max_completion_tokens` (includes reasoning tokens on reasoning models) |
| `"role": "system"` | MEDIUM | New `developer` role is preferred; `system` still works but is deprecated |
| `api_version="2024…"` | MEDIUM | Bump to a 2025‑era API version (e.g., `2025-06-01`) |
| `"gpt-4o"` | INFO | Update the model name after the code changes above are complete |

> The exact target‑model parameter behavior is captured in
> [`docs/05-api-changes-by-model.md`](../../docs/05-api-changes-by-model.md);
> use this script as a **first‑pass code scan**, then read that doc to apply
> the right per‑model changes.

## Usage

```bash
# Text report to stdout
python tools/audit/audit_codebase.py --path /path/to/your/app

# JSON output
python tools/audit/audit_codebase.py --path /path/to/your/app --format json --output audit.json

# Skip extra directories beyond the defaults
python tools/audit/audit_codebase.py --path . --exclude vendor build_artifacts
```

Exit code is **1** if any HIGH‑severity issues are found, making it easy to
wire into CI.

## Supported file types

`.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.cs`, `.java`, `.go`, `.rb`.

## What it does NOT do

- It does not call any model — it's purely a local file scan.
- It does not auto‑fix code (intentional — the right fix depends on the target
  model; see [API changes by model](../../docs/05-api-changes-by-model.md)).
- It does not understand call graphs, so a `temperature` flag may surface even
  if the parameter is later unset; review findings before bulk edits.
- It does not rewrite the SDK call shape itself — e.g.,
  `chat.completions.create(…) → responses.create(…)`. For that structural
  Chat Completions → Responses API migration, use
  [`tools/api-migration/`](../api-migration/), which ships an installable
  Agent Skill and a `migrate.py` scanner for that exact rewrite.
