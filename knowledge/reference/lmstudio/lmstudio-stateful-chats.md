---
type: API Endpoint
title: LM Studio Stateful Chats
description: Server-managed conversation state via response_id chaining.
tags: [lmstudio, rest, state, memory]
source: https://lmstudio.ai/docs/developer/rest/stateful-chats
timestamp: 2026-06-21
---

# LM Studio Stateful Chats

**Endpoint:** `POST /api/v1/chat` — **stateful by default**. The server stores conversation context per thread, so clients need not resend full history.

**Request fields:**
- `model` — model id.
- `input` — the new user message (string).
- `previous_response_id` — id of a prior response to continue from (optional).
- `store` — set `false` to disable persistence for one-off calls (optional).

**Response fields:**
- `model_instance_id` — loaded model.
- `output` — array of message objects (`type`, `content`).
- `response_id` — handle to reference this turn in later requests.

**Minimal example:**
```json
{ "model": "ibm/granite-4-micro", "input": "My favorite color is blue." }
```
Continue by passing the returned `response_id` as `previous_response_id`. Because any `response_id` can be referenced, conversations can **branch**.

Gotcha: server-side state lives in the LM Studio process, not your app — restarts/eviction may drop it; treat it as a cache, not the source of truth. (Verify retention/eviction semantics.)

**How The Clockwork Dark applies this:** This could offload our per-turn message rebuild and session memory — pass `previous_response_id` instead of replaying the whole transcript. Notably our `chat.end` event already mints a synthetic `response_id`, so the seam exists. **Regardless, `GameState` stays authoritative:** the deterministic engine owns dice, inventory, evil-phase, and travel; any server-side chat memory is a convenience layer we can rebuild from our own log at will.

Related: [[lmstudio-streaming-events]], [[lmstudio-integration-overview]]
