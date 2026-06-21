"""
LLM Response Schemas (PR23)
===========================

OpenAI-compatible ``response_format`` json-schema for the Storyteller turn
epilogue. When ``lmstudio.structured_output`` is enabled and the backend
supports constrained decoding, the model is forced to emit exactly this shape —
making our parsing bulletproof. The lenient parser (engine/agents/parsing.py)
remains the fallback for backends that ignore the schema.

See knowledge/reference/lmstudio/lmstudio-structured-output.md.
"""

from __future__ import annotations

from typing import Any

# The Storyteller turn epilogue contract as a JSON Schema.
STORYTELLER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "narration": {"type": "string"},
        "choices": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "text": {"type": "string"},
                },
                "required": ["id", "text"],
            },
        },
        "tool_calls": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "args": {"type": "object"},
                },
                "required": ["name"],
            },
        },
        "npc_voices": {"type": "array"},
        "stat_changes": {"type": "object"},
        "items_gained": {"type": "array"},
        "items_lost": {"type": "array"},
        "skill_check": {"type": ["object", "null"]},
        "tags_inline": {"type": "string"},
    },
    "required": ["narration", "choices"],
}

STORYTELLER_RESPONSE_FORMAT: dict[str, Any] = {
    "type": "json_schema",
    "json_schema": {
        "name": "clockwork_turn",
        "strict": True,
        "schema": STORYTELLER_SCHEMA,
    },
}
