---
type: API Endpoint
title: LM Studio Streaming Events
description: SSE event schema for the LM Studio REST chat stream.
tags: [lmstudio, rest, streaming, sse]
source: https://lmstudio.ai/docs/developer/rest/streaming-events
timestamp: 2026-06-21
---

# LM Studio Streaming Events

**Endpoint:** `POST /api/v1/chat` with `stream: true`. The response is **Server-Sent Events**, each frame formatted `event: <type>` then `data: <JSON>`.

The stream **always begins with `chat.start` and ends with `chat.end`**, events arriving in order. Roughly 20 event types group into lifecycle phases (verify exact list against the live docs):

- **`chat.start`** — carries `model_instance_id`.
- **`model_load.start|progress|end`** — load lifecycle; `progress` is a 0–1 float.
- **`prompt_processing.start|progress|end`** — prefill phases.
- **`reasoning.start|delta|end`** — reasoning text; `delta` has `content`.
- **`message.start|delta|end`** — assistant text; `delta` has `content`.
- **`tool_call.start|arguments|success|failure`** — `tool` name, `arguments` object, `output` string.
- **`error`** — structured `error` object.
- **`chat.end`** — aggregated `result`.

Every event has a `type` string equal to its name. Gotcha: this is LM Studio's **native** event vocabulary, distinct from OpenAI's `chat/completions` `data:`+`[DONE]` chunk stream.

**How The Clockwork Dark applies this:** Our `engine/lmstudio/client.py` currently consumes the **OpenAI-compatible** `/chat/completions` SSE (`data:` lines, `[DONE]`), then synthesizes its own typed `LMSStreamEvent`s (`chat.start`, `message.delta`, `chat.end`) — names that already mirror this native schema, easing migration. The `message.delta.content` deltas feed `ProseStreamGate` in `engine/agents/streaming.py`, which forwards prose live but gates the json epilogue. Adopting native events would give us first-class `reasoning.*` and `tool_call.*` frames for free.

Related: [[lmstudio-stateful-chats]], [[lmstudio-integration-overview]]
