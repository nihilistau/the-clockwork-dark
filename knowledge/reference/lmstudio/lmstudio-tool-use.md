---
type: API Endpoint
title: LM Studio Tool Use (tools / tool_calls)
description: Function-calling in OpenAI-compatible chat completions, with tool_choice control and tool-result round-trips.
tags: [lmstudio, openai-compat, tools, function-calling]
source: https://lmstudio.ai/docs/developer/openai-compat/tools
timestamp: 2026-06-21
---

# LM Studio Tool Use (tools / tool_calls)

**Endpoint:** `POST /v1/chat/completions`. Pass a `tools` array of `{"type": "function", "function": {name, description, parameters}}`, where `parameters` is a JSON Schema.

**tool_choice:** `"auto"` (model decides), `"none"` (never call tools), `"required"` (force tool-only output — **llama.cpp engines only**). (verify per engine.)

**Response:** When the model calls a tool, `choices[0].message.tool_calls` holds `[{id, type:"function", function:{name, arguments}}]` and `finish_reason` is `"tool_calls"`. Note `arguments` is a **JSON string**, not an object.

**Returning results:** Append the assistant message (with its `tool_calls`) then a message with `role:"tool"`, `tool_call_id` (matching the call `id`), and `content` (the result), and re-send.

**Gotchas (verify):** "Native" tool use requires a model whose chat template LM Studio supports; otherwise it falls back to a default `[TOOL_REQUEST]{...}[END_TOOL_REQUEST]` format. Malformed calls leak into `content` instead of `tool_calls`. With `stream:true`, tool-call fragments arrive piecemeal and must be accumulated.

**How The Clockwork Dark applies this:** The `tools` array maps cleanly onto our `@skill` registry — each skill's signature becomes one `function` entry, letting native `tool_calls` supersede the hand-rolled tool protocol in `tool_dispatcher.py`. The engine still resolves every call deterministically; the LLM only proposes them. `tool_choice:"required"` could force the Storyteller/Assistant to act through skills rather than freelancing prose, preserving our "engine resolves, LLMs narrate" rule.

Related: [[lmstudio-structured-output]], [[lmstudio-responses-api]]
