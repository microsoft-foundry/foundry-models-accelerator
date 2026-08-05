# 05. API Changes by Model

> **Source:** Adapted from
> [aiappsgbb/AOAI-models-migration/docs/api-changes-by-model.md](https://github.com/aiappsgbb/AOAI-models-migration/blob/main/docs/api-changes-by-model.md)
> with the GPT‑4o → GPT‑5.1 quick‑switch table folded in from
> [fatimataayeb/azure-openai-migration-guide](https://github.com/fatimataayeb/azure-openai-migration-guide).

Use this page as the **single matrix** indexed by *target model*. The
[`tools/audit/`](../tools/audit) script will tell you *where* in your code
each row applies.

## Parameter matrix

Legend: ✅ supported · ❌ remove · 🔄 renamed · ➕ new

| Parameter | `gpt-4o` | `gpt-4.1` | `gpt-5.x` (5.1 / 5.4 / 5.5) | o‑series |
|-----------|----------|-----------|-----------------------------|----------|
| `temperature` | ✅ | ✅ | ❌ | ❌ |
| `top_p` | ✅ | ✅ | ❌ | ❌ |
| `frequency_penalty` | ✅ | ✅ | ❌ | ❌ |
| `presence_penalty` | ✅ | ✅ | ❌ | ❌ |
| `logprobs` | ✅ | ✅ | ❌ | ❌ |
| `max_tokens` | ✅ | ✅ | 🔄 `max_completion_tokens` | 🔄 `max_completion_tokens` |
| `role: "system"` | ✅ | ✅ | ✅ works; `developer` preferred | ✅ same |
| `reasoning_effort` | — | — | ➕ `none \| low \| medium \| high` (`gpt-5.1` defaults `none`; `minimal` is original‑GPT‑5 only) | ➕ `low \| medium \| high` |
| `response_format` (structured outputs) | ✅ | ✅ | ✅ | ✅ |
| Tool / function calling | ✅ | ✅ | ✅ | ✅ |

## Client / API version

| Target | Recommended `api_version` | Notes |
|--------|---------------------------|-------|
| `gpt-4.1` | `2025-06-01` | Same chat surface as 4o |
| `gpt-5.x` | `2025-06-01` | Reasoning models — drop sampling knobs |
| o‑series | `2025-06-01` | Pure reasoning — no `temperature`, `top_p`, etc. |

The v1 GA endpoint shape (`…/openai/v1/…`, no `api-version` in URL) is the
recommended target. See [`docs/01-methodology/discovery.md`](./01-methodology/discovery.md)
§ 7 for migrating the URL pattern itself.

---

## GPT‑4o → GPT‑5.1 quick‑switch (from #3)

> **Source:** condensed from
> [fatimataayeb/azure-openai-migration-guide README](https://github.com/fatimataayeb/azure-openai-migration-guide#%EF%B8%8F-what-needs-to-change).
> For a full before/after Python example see
> [`examples/before-after/gpt4o_to_gpt51.md`](../examples/before-after/gpt4o_to_gpt51.md).

| Change | Before (GPT‑4o) | After (GPT‑5.1) | Why |
|--------|-----------------|-----------------|-----|
| API Version | `2024-10-21` | `2025-06-01` | New features support |
| Model Name | `gpt-4o` | `gpt-5.1` | New model |
| System Role | `"system"` | `"developer"` | Improved clarity |
| Max Tokens | `max_tokens` | `max_completion_tokens` | Now includes reasoning tokens |
| Sampling | `temperature=0.7` | _(remove)_ | Use `reasoning_effort` instead |
| New | _(n/a)_ | `reasoning_effort="low"` | Controls reasoning depth |

## SDKs other than Python

Per‑SDK code snippets (C#, JS/TS, Java) live under
[`examples/sdks/`](../examples/sdks/). The shape of the changes is the same as
the Python table above.

---

## Chat Completions → Responses API

> **Source:** Adapted from
> [Azure-Samples/azure-openai-to-responses](https://github.com/Azure-Samples/azure-openai-to-responses).
> The upstream repo also ships an installable Agent Skill and a `migrate.py`
> scanner that automates these edits — see
> [`tools/api-migration/`](../tools/api-migration/).

GPT‑5.x and newer models require the **Responses API**, not Chat Completions.
This is a structural change to the SDK surface, independent of any parameter
matrix above: even if every parameter were identical, the request and
response shapes are different.

The recommended target shape on Azure today is the **OpenAI client pointed at
the Azure v1 GA endpoint**: `…/openai/v1/responses`, with no `api_version` to
manage.

### Mapping table

| Concern | Before — Chat Completions | After — Responses API |
|---------|---------------------------|-----------------------|
| Python client | `from openai import AzureOpenAI` <br/> `client = AzureOpenAI(api_key=…, api_version="2024-…", azure_endpoint=…)` | `from openai import OpenAI` <br/> `client = OpenAI(api_key=…, base_url="https://<resource>.openai.azure.com/openai/v1/")` |
| `api_version` | Required in URL or client | **Not used** on v1 GA endpoint |
| Endpoint path | `…/openai/deployments/{deployment}/chat/completions` | `…/openai/v1/responses` |
| Call | `client.chat.completions.create(model=…, messages=[…])` | `client.responses.create(model=…, input=…)` |
| Input field | `messages=[{"role": "user", "content": …}, …]` | `input=…` (string, array of blocks, or message list) |
| Output access | `resp.choices[0].message.content` | `resp.output_text` |
| Streaming | `for chunk in client.chat.completions.create(..., stream=True):` | `for event in client.responses.create(..., stream=True):` (event‑typed stream) |
| Tools / function calling | `tools=[…]`, `tool_choice=…` | `tools=[…]`, `tool_choice=…` *(carries over; richer tool integration on the Responses side)* |
| Structured outputs | `response_format={"type": "json_schema", …}` | `response_format={"type": "json_schema", …}` *(carries over and is the recommended shape on Responses)* |
| Reasoning controls | n/a | `reasoning={"effort": "low \| medium \| high"}` |
| `max_tokens` | `max_tokens=…` | `max_output_tokens=…` |

### Minimal before / after (Python)

```python
# Before — Azure OpenAI client + Chat Completions
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-10-21",
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Say hi."}],
    max_tokens=200,
    temperature=0.7,
)
text = resp.choices[0].message.content
```

```python
# After — OpenAI client + Responses API on Azure v1 GA endpoint
from openai import OpenAI

client = OpenAI(
    api_key=AZURE_OPENAI_KEY,
    base_url=f"{AZURE_OPENAI_ENDPOINT}/openai/v1/",
)

resp = client.responses.create(
    model="gpt-5.1",
    input="Say hi.",
    max_output_tokens=200,
    reasoning={"effort": "low"},  # replaces temperature/top_p on reasoning models
)
text = resp.output_text
```

### When you don't need the Responses API yet

You can stay on Chat Completions while your target is still in the GPT‑4
family (`gpt-4o`, `gpt-4.1`). Move to Responses when:

- Your target is GPT‑5.x, an o‑series reasoning model, or anything newer that
  documents Responses‑only support.
- You want to consolidate on the v1 GA endpoint and drop `api_version`
  management.
- You need richer tool integration or the event‑typed streaming shape.

### Compatibility caveats

The upstream repo documents per‑model and per‑region quirks that matter in
production. The non‑obvious ones:

- **Older models** may not support every Responses API capability (e.g.,
  certain streaming event types or tool shapes). Cross‑check with
  [`tools/availability/`](../tools/availability/) for the live per‑model
  picture.
- **Reasoning / o‑series parameters** (`reasoning.effort`, removal of
  `temperature` / `top_p`) interact with the Responses surface — see the
  parameter matrix at the top of this page and the upstream support matrix.
- **Frontend code** usually does **not** need to change if the server
  collapses the response to a string before returning it. It *does* change
  when the frontend consumes streaming events directly.

### How to apply this change

| Step | Use |
|------|-----|
| Find the call sites | [`tools/audit/`](../tools/audit/) (parameter‑level), then [`tools/api-migration/`](../tools/api-migration/) (call‑shape level) |
| Rewrite the calls | [`tools/api-migration/`](../tools/api-migration/) — Agent Skill (interactive) or `migrate.py` (batch) |
| Verify the change | Mirror the upstream `demo/openai-chat-app-quickstart` sample; then run [`tools/evaluator/`](../tools/evaluator/) against your golden dataset |
| Confirm regional support | [`tools/availability/`](../tools/availability/) — Responses API support matrix by model × region |
