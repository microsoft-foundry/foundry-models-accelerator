# GPT‑4o → GPT‑5.1

> **Source:** Adapted from
> [fatimataayeb/azure-openai-migration-guide](https://github.com/fatimataayeb/azure-openai-migration-guide).

## Python (OpenAI SDK)

### Before — GPT‑4o

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_version="2024-10-21",
    azure_endpoint="https://my-aoai.openai.azure.com/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize this incident report in three bullets."},
    ],
    temperature=0.7,
    max_tokens=500,
)
```

### After — GPT‑5.1

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_version="2025-06-01",         # bump
    azure_endpoint="https://my-aoai.openai.azure.com/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

response = client.chat.completions.create(
    model="gpt-5.1",                  # bump
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},  # system → developer
        {"role": "user", "content": "Summarize this incident report in three bullets."},
    ],
    max_completion_tokens=500,        # max_tokens → max_completion_tokens
    reasoning_effort="low",           # optional — gpt-5.1 defaults to "none" (fastest)
    # temperature: REMOVE — unsupported on the GPT-5 family
)
```

## Diff summary

| Change | Before | After | Why |
|--------|--------|-------|-----|
| API version | `2024-10-21` | `2025-06-01` | New features support |
| Model name | `gpt-4o` | `gpt-5.1` | New model |
| Role name | `"system"` | `"developer"` | Preferred (`system` still supported) |
| Output cap | `max_tokens` | `max_completion_tokens` | Now includes reasoning tokens |
| Sampling | `temperature=0.7` | _(remove)_ | Use `reasoning_effort` instead |
| New | _(n/a)_ | `reasoning_effort="low"` | Control reasoning depth |

> **On `reasoning_effort`:** `gpt-5.1` defaults `reasoning_effort` to `none`,
> which is the fastest, most `gpt-4o`‑like behavior (no reasoning tokens
> billed). This example passes `"low"` to opt into light reasoning; raise it
> only when the workload needs it. `minimal` is **not** supported on `gpt-5.1`
> (it's original‑GPT‑5 only).

Run [`tools/audit/audit_codebase.py`](../../tools/audit/audit_codebase.py)
against your code to find every place the table above needs to be applied.
