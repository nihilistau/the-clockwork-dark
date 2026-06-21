---
type: Architecture
title: LM Studio Integration Overview
description: How The Clockwork Dark talks to a local OpenAI-compatible LLM today, and migration paths.
tags: [lmstudio, rest, architecture, llm]
source: https://lmstudio.ai/docs/developer/rest
timestamp: 2026-06-21
---

# LM Studio Integration Overview

**Today.** `engine/lmstudio/client.py` (`LMSClient`) calls `POST {base_url}/chat/completions` with `stream: true` against LM Studio's **OpenAI-compatible** endpoint (`http://localhost:1234/v1`). It parses `data:` SSE lines until `[DONE]`, yields `delta.content`, and emits typed `LMSStreamEvent`s (`chat.start`/`message.delta`/`chat.end`/`error`). Health is a `GET /models` probe; it degrades gracefully offline for tests. Auth via `api_key` (config `lmstudio.api_key` or `LMSTUDIO_API_KEY`).

**Profiles** (`profiles.py`): `big` (narration), `small` (terse), `draft` (fast skeleton). **Speculative** (`speculative.py`): a `draft` pass outlines a 1–2 sentence skeleton, injected as a system hint into the `big` **refine** stream; falls back to refine-only if draft fails.

**Governance loop.** The Storyteller streams prose followed by a fenced json epilogue. `ProseStreamGate` (`engine/agents/streaming.py`) forwards prose live while withholding the epilogue, which the engine parses ([[okfs-spec]]-adjacent `engine/agents/parsing.py`) and validates before mutating `GameState` (authoritative). Note: a model that emits *pure* JSON (no prose preamble) yields nothing to stream — resolved by the structured-output migration.

**Migration opportunities** unlocked by the sibling concepts:
- **Native streaming events** ([[lmstudio-streaming-events]]) — first-class `reasoning.*` and `tool_call.*` frames.
- **Stateful chats** ([[lmstudio-stateful-chats]]) — `previous_response_id` offloads transcript rebuild (state still mirrored in `GameState`).
- **Native structured-output + tool-calls** ([[lmstudio-structured-output]], [[lmstudio-tool-use]]) — replace the JSON-epilogue with schema-constrained output and real tool invocations.
- **MCP + cancellation** ([[lmstudio-mcp-host]], [[lmstudio-cancelling-predictions]]) — standardized tool transport and mid-stream abort.

We own server and client, so this stays provider-agnostic. See [[llm-migration-plan]].

Related: [[lmstudio-streaming-events]], [[lmstudio-stateful-chats]]
