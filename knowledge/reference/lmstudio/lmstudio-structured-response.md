---
type: Reference
title: LM Studio Structured Response (Python SDK)
description: Schema-enforced JSON output via response_format and .parsed in lmstudio-python.
tags: [lmstudio, python, structured-output, json-schema]
source: https://lmstudio.ai/docs/python/llm-prediction/structured-response
timestamp: 2026-06-21
---

# LM Studio Structured Response (Python SDK)

Forces model output to conform to a schema, so the result is reliably machine-parseable instead of free prose.

**Key API surface:**
- `response_format=` kwarg on `.respond()` — accepts a Pydantic `BaseModel` subclass, `lmstudio.BaseModel`, or a raw JSON-schema dict.
- ModelSchema protocol — any class exposing a `model_json_schema()` classmethod works (Pydantic and msgspec satisfy this).
- `result.parsed` — the structured payload as a string-keyed dict conforming to the schema.
- Works in both streaming and non-streaming modes.

```python
from pydantic import BaseModel
import lmstudio as lms

class BookSchema(BaseModel):
    title: str
    author: str
    year: int

model = lms.llm()
result = model.respond("Tell me about The Hobbit", response_format=BookSchema)
book = result.parsed  # dict conforming to BookSchema
```

**Gotchas:** enforcement depends on the loaded model/runtime supporting constrained decoding; verify behavior per model. `parsed` is a dict — re-validate into the Pydantic instance yourself if you need typed access.

**How The Clockwork Dark applies this:** This is a candidate replacement for our hand-rolled JSON-epilogue parsing in `engine/agents/parsing.py`, which today repairs fenced/messy JSON from local models heuristically. The provider-agnostic equivalent is to pass an OpenAI-style `response_format` (json_schema) on our `LMSClient.chat` payload so the Storyteller epilogue (`narration`/`choices`/`tool_calls`) arrives schema-valid. Keep the lenient parser as a fallback for backends that ignore the schema; do not assume the `lmstudio` SDK.

Related: [[lmstudio-chat-completion]]
