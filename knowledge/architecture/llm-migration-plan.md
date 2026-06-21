---
type: Decision
title: LLM Layer Migration Plan
description: Move from hand-rolled JSON-epilogue parsing toward native structured output, tool-calls, and MCP.
tags: [architecture, llm, decision, tools, structured-output]
resource: engine/agents/parsing.py
timestamp: 2026-06-21
---

# LLM Layer Migration Plan

**Today** the Storyteller emits prose + a fenced `json` epilogue that we parse
leniently (`engine/agents/parsing.py`) and dispatch (`tool_dispatcher.py`). This
works on weak local models but is heuristic. Three capabilities — all reachable
over the OpenAI-compatible REST API, so **provider-agnostic** — let us tighten
it without locking to LM Studio (we own both server and client).

## Opportunities (ranked)
1. **Native structured output** ([[lmstudio-structured-output]],
   [[lmstudio-structured-response]]) — pass `response_format: json_schema` so the
   epilogue arrives schema-valid. Keep the lenient parser as a fallback for
   backends that ignore the schema. Biggest reliability win, smallest change.
2. **Native tool-calls** ([[lmstudio-tool-use]]) — render the `@skill` registry
   as an OpenAI `tools` array; consume `message.tool_calls` instead of parsing
   tool intents from prose. `tool_choice: "required"` can force "engine resolves,
   LLM narrates." Larger change to `tool_dispatcher.py`.
3. **MCP + agentic loop** ([[lmstudio-mcp-host]], [[lmstudio-act-agentic-loop]])
   — expose skills via an ephemeral MCP server; or model our own `.act()`-style
   multi-round loop. Highest ceiling, most infra.

## Adjacent wins
- **Cancellation / budget** ([[lmstudio-cancelling-predictions]]) — drain-and-emit
  partial narration when `TurnBudget` trips, rather than hard-abort.
- **Stateful chats** ([[lmstudio-stateful-chats]]) — `previous_response_id`
  offloads transcript rebuild; `GameState` stays authoritative regardless.
- **Native streaming events** ([[lmstudio-streaming-events]]) — first-class
  `reasoning.*` / `tool_call.*` frames.

## Principle
Every step stays behind our `LMSClient` seam and a config switch. The engine
remains the source of truth; the LLM only ever proposes.
