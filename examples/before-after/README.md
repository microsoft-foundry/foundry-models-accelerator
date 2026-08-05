# Before / After code examples

Per‑target‑model code diffs showing the minimum changes to move off GPT‑4o.
For the underlying *parameter rationale* see
[`docs/05-api-changes-by-model.md`](../../docs/05-api-changes-by-model.md).

| Target model | File |
|--------------|------|
| GPT‑5.1 | [`gpt4o_to_gpt51.md`](./gpt4o_to_gpt51.md) |
| GPT‑4.1, GPT‑5.4, GPT‑5.5, o‑series | _coming when the upstream samples are folded in from #4_ |

> The 5.1 example is adapted from
> [fatimataayeb/azure-openai-migration-guide](https://github.com/fatimataayeb/azure-openai-migration-guide).
> Per‑target diffs for 4.1 / 5.4 / 5.5 / o‑series will land when the upstream
> samples from
> [aiappsgbb/AOAI-models-migration](https://github.com/aiappsgbb/AOAI-models-migration)
> are folded in via `git subtree`.

## Chat Completions → Responses API

For a **fully migrated end‑to‑end sample app** (Python backend + frontend,
covering streaming, structured outputs, and tools) see
`demo/openai-chat-app-quickstart` in
[Azure‑Samples/azure‑openai‑to‑responses](https://github.com/Azure-Samples/azure-openai-to-responses).
The canonical mapping table is in
[`docs/05-api-changes-by-model.md`](../../docs/05-api-changes-by-model.md) §
*Chat Completions → Responses API*, and the tooling to apply the change to
your own codebase lives in [`tools/api-migration/`](../../tools/api-migration/).
