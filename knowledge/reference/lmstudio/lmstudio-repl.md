---
type: Reference
title: LM Studio Python REPL / Getting Started
description: Interactive convenience-API usage of lmstudio-python in the Python REPL.
tags: [lmstudio, python, repl, getting-started]
source: https://lmstudio.ai/docs/python/getting-started/repl
timestamp: 2026-06-21
---

# LM Studio Python REPL / Getting Started

Shows how to drive lmstudio-python interactively. The convenience API auto-manages resources via `atexit` hooks, so no `with` blocks are needed in a REPL session.

**Key API surface:**
- Launch the standard Python REPL; for async use `python -m asyncio` (requires SDK >= 1.5.0).
- `import lmstudio as lms`
- `lms.list_loaded_models()` — returns currently loaded models; index `[0]` for the first.
- `lms.Chat("system prompt")` — chat session; `chat.add_user_message(...)`.
- `model.respond(chat, on_message=chat.append)` — generate and append the reply back into context, enabling multi-turn.

```python
import lmstudio as lms
model = lms.list_loaded_models()[0]
chat = lms.Chat("You answer questions concisely")
chat.add_user_message("Tell me three fruits")
print(model.respond(chat, on_message=chat.append))
```

**Gotchas:** the synchronous convenience API is intended for REPL/Jupyter; production code should use the scoped-resource API with `with` statements. Chat context persists across REPL commands.

**How The Clockwork Dark applies this:** This is a developer-ergonomics reference, not a runtime dependency. Our equivalent quick-poke loop hits `LMSClient` (e.g. `get_lms_client().chat(...)` / `is_available()`) against the OpenAI-compatible endpoint, and `list_loaded_models()` maps to our `GET /models` health check. Useful as a manual smoke-test pattern during vertical-slice playtesting; keep any such REPL helpers SDK-free so they exercise the same provider-agnostic path as the game.

Related: [[lmstudio-chat-completion]]
