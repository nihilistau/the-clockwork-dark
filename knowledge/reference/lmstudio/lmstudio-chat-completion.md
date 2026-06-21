---
type: Reference
title: LM Studio Chat Completions (Python SDK)
description: Multi-turn chat generation via model.respond / respond_stream in lmstudio-python.
tags: [lmstudio, python, chat, streaming]
source: https://lmstudio.ai/docs/python/llm-prediction/chat-completion
timestamp: 2026-06-21
---

# LM Studio Chat Completions (Python SDK)

Drives multi-turn conversations against a loaded local model. You obtain a model handle with `lms.llm()` (or `lms.llm("model-name")`), build context with the `lms.Chat` class, and generate replies.

**Key API surface:**
- `lms.llm()` / `lms.llm("qwen2.5-7b-instruct")` — get a model handle.
- `lms.Chat("system prompt")` — conversation object; `chat.add_user_message(...)` appends turns.
- `model.respond(chat)` — synchronous, non-streaming; returns a result.
- `model.respond_stream(chat)` — synchronous streaming; iterates token *fragments*. Async variants exist.
- `config=` kwarg — inference settings like `temperature`, `maxTokens` (note camelCase in SDK config).
- Callbacks: `on_prompt_processing_progress`, `on_first_token`, `on_prediction_fragment`, `on_message`.
- `result.stats` — `predicted_tokens_count`, `time_to_first_token_sec`, `stop_reason`, `model_info.display_name`.

```python
import lmstudio as lms
model = lms.llm()
print(model.respond("What is the meaning of life?"))
```

**Gotchas:** the convenience API is REPL/Jupyter-oriented; verify exact config key casing against the SDK. Streaming yields fragments, not whole messages.

**How The Clockwork Dark applies this:** This maps directly to our provider-agnostic `LMSClient.chat` / `chat_stream` in `engine/lmstudio/client.py`, which we implement over the raw OpenAI-compatible `POST /chat/completions` SSE endpoint rather than the `lmstudio` SDK. The SDK's `on_prediction_fragment`/`on_message` callbacks parallel our `on_event` (`LMSStreamEvent`) hooks and `result.stats` parallels our `latency_ms`/stats payload. Treat the SDK as a reference contract for any future backend swap, not a hard dependency.

Related: [[lmstudio-structured-response]]
