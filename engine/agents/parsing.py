"""
Robust LLM Output Parsing (PR16)
================================

Real local models are messy: they fence JSON inconsistently, nest objects the
old non-greedy regex truncated, emit trailing commas / smart quotes, vary the
tool-call shape (``name`` vs ``skill``, flat vs nested ``args``, OpenAI
``function``), or skip the JSON epilogue entirely. This module turns any of that
into a stable Storyteller dict, never raising — worst case it degrades to
prose-only with default choices.

Public surface:
  * ``parse_storyteller_response(raw) -> dict`` — the epilogue contract dict
  * ``normalize_tool_calls(raw_calls) -> list[dict]`` — uniform {name, args}
  * ``extract_balanced_objects(text) -> list[tuple[int,int]]`` — span scanner

Version: v0.3.0 [2026-06-21]
"""

from __future__ import annotations

import json
import re
from typing import Any, Optional

_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)
_TRAILING_COMMA = re.compile(r",(\s*[}\]])")
_SMART_QUOTES = {
    "“": '"', "”": '"', "‘": "'", "’": "'",
    "–": "-", "—": "-", " ": " ",
}

# Keys the Storyteller epilogue must carry; missing ones get safe defaults.
_DEFAULTS: dict[str, Any] = {
    "narration": "",
    "choices": [],
    "tool_calls": [],
    "npc_voices": [],
    "stat_changes": {},
    "items_gained": [],
    "items_lost": [],
    "skill_check": None,
    "tags_inline": "",
}

_FALLBACK_CHOICES = [
    {"id": "a", "text": "Look around"},
    {"id": "b", "text": "Continue"},
]


def extract_balanced_objects(text: str) -> list[tuple[int, int]]:
    """Return (start, end) spans of every balanced top-level ``{...}`` object.

    Brace counting respects double-quoted strings and escapes, so nested objects
    no longer truncate the match (the bug in the old ``{.*?}`` regex).
    """
    spans: list[tuple[int, int]] = []
    i, n = 0, len(text)
    while i < n:
        if text[i] != "{":
            i += 1
            continue
        depth, in_str, esc, j = 0, False, False, i
        while j < n:
            c = text[j]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            elif c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    spans.append((i, j + 1))
                    break
            j += 1
        i = j + 1
    return spans


def _loads_lenient(blob: str) -> Optional[dict[str, Any]]:
    """json.loads with a light repair pass (smart quotes, trailing commas)."""
    for attempt in (blob, _repair(blob)):
        try:
            data = json.loads(attempt)
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, ValueError):
            continue
    return None


def _repair(blob: str) -> str:
    for bad, good in _SMART_QUOTES.items():
        blob = blob.replace(bad, good)
    return _TRAILING_COMMA.sub(r"\1", blob)


def _candidate_objects(raw: str) -> list[tuple[int, int, str]]:
    """Yield (start, end, blob) JSON-object candidates, best last.

    Prefers objects inside ```json fences, then any balanced object that
    mentions ``"narration"`` (the epilogue), falling back to all objects.
    """
    candidates: list[tuple[int, int, str]] = []
    for m in _FENCE.finditer(raw):
        inner = m.group(1)
        for s, e in extract_balanced_objects(inner):
            candidates.append((m.start(1) + s, m.start(1) + e, inner[s:e]))
    for s, e in extract_balanced_objects(raw):
        candidates.append((s, e, raw[s:e]))
    # epilogue objects (those naming narration/choices/tool_calls) rank highest
    keyed = [c for c in candidates if '"narration"' in c[2] or '"choices"' in c[2]
             or '"tool_calls"' in c[2]]
    return keyed or candidates


def normalize_tool_calls(raw_calls: Any) -> list[dict[str, Any]]:
    """Coerce any tool-call shape into a uniform ``[{"name", "args"}]`` list."""
    if not isinstance(raw_calls, list):
        return []
    out: list[dict[str, Any]] = []
    for call in raw_calls:
        if not isinstance(call, dict):
            continue
        name = (
            call.get("name")
            or call.get("skill")
            or call.get("tool")
            or call.get("function")
        )
        if isinstance(name, dict):  # OpenAI: {"function": {"name", "arguments"}}
            args_src = name.get("arguments")
            name = name.get("name")
        else:
            args_src = (
                call.get("args")
                or call.get("arguments")
                or call.get("parameters")
                or call.get("input")
                or {}
            )
        if not name or not isinstance(name, str):
            continue
        if isinstance(args_src, str):
            args_src = _loads_lenient(args_src) or {}
        if not isinstance(args_src, dict):
            args_src = {}
        out.append({"name": name.strip(), "args": args_src})
    return out


def _prose_before(raw: str, json_start: int) -> str:
    """Narration = text before the epilogue, stripped of code fences/labels."""
    prefix = raw[:json_start]
    prefix = _FENCE.sub("", prefix)
    prefix = prefix.replace("```json", "").replace("```", "")
    return prefix.strip()


def parse_storyteller_response(raw: str) -> dict[str, Any]:
    """Parse a Storyteller LLM response into the epilogue contract dict.

    Never raises. If no JSON is found, returns prose-only with default choices.
    """
    raw = raw or ""
    for start, _end, blob in reversed(_candidate_objects(raw)):
        data = _loads_lenient(blob)
        if data is None:
            continue
        out = {**_DEFAULTS, **data}
        out["tool_calls"] = normalize_tool_calls(out.get("tool_calls"))
        if not out.get("narration"):
            out["narration"] = _prose_before(raw, start) or raw.strip()
        if not isinstance(out.get("choices"), list):
            out["choices"] = []
        return out

    # No parseable JSON at all → prose-only fallback.
    prose = _FENCE.sub("", raw).strip() or raw.strip()
    return {**_DEFAULTS, "narration": prose, "choices": list(_FALLBACK_CHOICES)}
