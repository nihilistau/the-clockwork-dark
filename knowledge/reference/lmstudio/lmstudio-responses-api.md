---
type: API Endpoint
title: LM Studio Responses API (/v1/responses)
description: Stateful, reasoning-aware generation endpoint with a single input field and Remote MCP tools.
tags: [lmstudio, openai-compat, responses, reasoning]
source: https://lmstudio.ai/docs/developer/openai-compat/responses
timestamp: 2026-06-21
---

# LM Studio Responses API (/v1/responses)

**Endpoint:** `POST /v1/responses`. An alternative to chat completions that takes a single `input` string instead of a `messages` array, and adds reasoning and stateful continuation.

**Request shape:**
```json
{
  "model": "openai/gpt-oss-20b",
  "input": "Provide a prime number less than 50",
  "reasoning": { "effort": "low|medium|high" },
  "previous_response_id": "<id>",
  "stream": true,
  "tools": [ { "type": "mcp" } ]
}
```
`model` and `input` are required; the rest optional.

**Response:** Non-streaming returns a full response object. Streaming (`stream:true`) emits SSE events: `response.created`, `response.output_text.delta`, `response.completed`.

**Features:** Streaming; reasoning via `reasoning.effort`; **Remote MCP** tools via `tools` with `type:"mcp"`; stateful follow-ups via `previous_response_id`. Structured output is not explicitly documented for this endpoint (verify).

**Gotchas (verify):** Remote MCP tools require explicit opt-in in app settings. Stateful chaining depends on retaining the prior `previous_response_id`.

**How The Clockwork Dark applies this:** Reasoning `effort` and server-side stateful continuation could let our autonomous agents (`clockwork_storyteller`, `clockwork_assistant`) carry turn-to-turn context without us re-sending full transcripts, trimming token cost. We'd keep our config-driven endpoint selection (`config/default.yaml`) so we can choose `/v1/responses` or `/v1/chat/completions` per provider. Its Remote MCP `tools` overlaps conceptually with our `@skill` registry, but our deterministic engine — not a remote MCP server — must stay the authority over dice, combat, and travel.

Related: [[lmstudio-tool-use]], [[lmstudio-structured-output]]
