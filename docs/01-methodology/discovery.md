# A. Discovery — Understand the application and current model usage

> **Source:** Adapted from
> [saurabhvartak1982/modelmigration § A](https://github.com/saurabhvartak1982/modelmigration#a-discovery-understand-the-application-and-current-model-usage).

Before changing anything, capture how the workload actually uses the current
model. Use the discovery scanner ([`tools/discovery/`](../../tools/discovery))
to get an inventory; use this checklist to fill in the application context the
scanner cannot see.

## 1. Workload type & modality needs

- What does the app do (chat/Q&A, RAG, extraction, summarization, coding
  assistant, agentic orchestration)?
- What modalities are used or required (text, vision, audio, etc.)?

## 2. Interaction pattern

- Stateless single‑turn vs multi‑turn conversation (is history included?)
- RAG vs non‑RAG
- Tool/function calling or not (and how many tools)

## 3. Architecture & rollout feasibility

- Can you run parallel deployments (blue/green, canary, A/B)?
- Where can traffic be split (app layer, APIM, gateway, service mesh)?

## 4. Token profile and context-window fit

- Current p50/p95/max input tokens (prompt + history + RAG docs + tool schemas)
- Current output length and `max_output_tokens` / `max_tokens` usage
- Validate: effective output = `min(max_output, context_window − input_tokens)`

## 5. Output contract requirements

- Do you rely on "prompted JSON" (format described in instructions) or strict
  structured outputs?
- Any schema validation in code? (required keys, enums, ordering assumptions, …)

## 6. Model + deployment constraints

- Current model family and candidate target model(s)
- Deployment type: **Standard / PTU / Batch** + **Regional / Global / Data Zone**
- Region/location boundaries and compliance requirements
- Quota posture (TPM/RPM) and headroom

## 7. API surface / URL pattern used by the app

- Legacy: `…/openai/deployments/{deployment}/… ?api-version=YYYY-MM-DD`
- v1 GA: `…/openai/v1/…` where `api-version` is not required
- Is `api-version` hardcoded in URL, config, or SDK parameter?

## 8. How the deployment name is referenced

- Is the deployment name provided as a parameter/config (so the SDK builds the
  URL), or embedded directly in URL / `base_url`?
- This determines how large the code/config change will be.

## 9. Baseline quality, performance, and known issues

- How was the current model validated? Any golden dataset? Edge cases?
- How was the earlier model and application performance tested?
- Any production pain points (latency, cost spikes, JSON validity,
  hallucinations, tool‑call mistakes)?
- Any reliability incidents tied to input size / tool schemas?

---

→ Once you have the inventory and answers above, move on to
[**B. Delta analysis**](./delta.md).
