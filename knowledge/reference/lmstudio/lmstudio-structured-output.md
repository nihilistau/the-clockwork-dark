---
type: API Endpoint
title: LM Studio Structured Output (response_format json_schema)
description: Force OpenAI-compatible chat completions to emit JSON validated against a supplied JSON Schema.
tags: [lmstudio, openai-compat, structured-output, json-schema]
source: https://lmstudio.ai/docs/developer/openai-compat/structured-output
timestamp: 2026-06-21
---

# LM Studio Structured Output (response_format json_schema)

**Endpoint:** `POST /v1/chat/completions`. Add a `response_format` object to the standard chat-completions body to constrain output to a schema.

**Request shape:**
```json
"response_format": {
  "type": "json_schema",
  "json_schema": {
    "name": "joke_response",
    "strict": "true",
    "schema": {
      "type": "object",
      "properties": { "joke": { "type": "string" } },
      "required": ["joke"]
    }
  }
}
```
Fields: `type` (`"json_schema"`), and `json_schema` with `name`, `strict`, and a JSON Schema `schema`.

**Response:** The validated JSON arrives as a **string** in `choices[0].message.content` — you must `JSON.parse`/`json.loads` it; it is not pre-deserialized.

**Gotchas (verify):** Not all models can do structured output — sub-7B LLMs often fail. Enforcement engine differs by format: GGUF models use grammar-based (GBNF) sampling; MLX models use Outlines. The schema must itself be valid. `strict` is shown as the string `"true"` in the docs.

**How The Clockwork Dark applies this:** This could replace our brittle JSON-epilogue parsing in `engine/lmstudio/client.py` with guaranteed-valid output for any structured handoff (skill calls, state deltas, evil-phase transitions). Because it rides the OpenAI-compat `response_format` field, it stays provider-agnostic. We'd still parse `content` as a string, so the engine remains the source of truth and merely gains schema-shaped, lower-retry LLM responses.

Related: [[lmstudio-tool-use]]
