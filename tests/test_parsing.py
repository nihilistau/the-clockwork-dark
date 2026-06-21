"""Robust Storyteller output parsing (PR16)."""

from __future__ import annotations

from engine.agents.parsing import (
    extract_balanced_objects,
    normalize_tool_calls,
    parse_storyteller_response,
)

# Storyteller's run_turn imports the re-export — make sure it still works.
from engine.agents.storyteller import parse_storyteller_response as st_parse


def test_reexport_matches():
    assert st_parse is parse_storyteller_response


def test_clean_fenced_json():
    raw = """Some preamble.
```json
{"narration": "The mist parts.", "choices": [{"id": "a", "text": "Walk"}], "tool_calls": []}
```"""
    out = parse_storyteller_response(raw)
    assert out["narration"] == "The mist parts."
    assert out["choices"][0]["text"] == "Walk"


def test_nested_objects_do_not_truncate():
    # The old `{.*?}` regex stopped at the first '}', losing choices.
    raw = """```json
{"narration": "n", "stat_changes": {"hp": {"delta": -2, "reason": "thorn"}},
 "skill_check": {"skill": "nerve", "dc_mod": 1},
 "choices": [{"id": "a", "text": "Press on"}, {"id": "b", "text": "Rest"}]}
```"""
    out = parse_storyteller_response(raw)
    assert out["stat_changes"]["hp"]["delta"] == -2
    assert len(out["choices"]) == 2
    assert out["skill_check"]["skill"] == "nerve"


def test_unfenced_json_with_prose_prefix():
    raw = 'You step into the clearing.\n{"narration": "", "choices": []}'
    out = parse_storyteller_response(raw)
    # narration falls back to the prose before the epilogue
    assert "clearing" in out["narration"]


def test_trailing_commas_and_smart_quotes_repaired():
    raw = '{“narration”: “Smoke threads the birch.”, “choices”: [],}'
    out = parse_storyteller_response(raw)
    assert "Smoke" in out["narration"]


def test_prose_only_falls_back_to_choices():
    raw = "The forest holds its breath. Nothing stirs."
    out = parse_storyteller_response(raw)
    assert out["narration"].startswith("The forest")
    assert len(out["choices"]) == 2  # default fallback choices


def test_empty_input_safe():
    out = parse_storyteller_response("")
    assert out["narration"] == ""
    assert out["choices"]  # defaults provided


def test_extract_balanced_objects_handles_braces_in_strings():
    text = 'x {"a": "has } brace", "b": {"c": 1}} y'
    spans = extract_balanced_objects(text)
    assert len(spans) == 1
    s, e = spans[0]
    assert text[s:e] == '{"a": "has } brace", "b": {"c": 1}}'


def test_picks_epilogue_over_incidental_object():
    raw = 'Earlier {"unrelated": 1} text.\n```json\n{"narration": "real", "choices": []}\n```'
    out = parse_storyteller_response(raw)
    assert out["narration"] == "real"


def test_normalize_tool_calls_name_variants():
    calls = [
        {"name": "roll_dice", "args": {"sides": 20}},
        {"skill": "move_to", "arguments": {"location_id": "edgewood_square"}},
        {"tool": "trade", "parameters": {"action": "browse"}},
        {"function": {"name": "query_evil_state", "arguments": "{}"}},
        {"name": "craft_item", "args": '{"recipe_id": "herb_poultice"}'},
        "garbage",
        {"no_name": True},
    ]
    out = normalize_tool_calls(calls)
    names = [c["name"] for c in out]
    assert names == ["roll_dice", "move_to", "trade", "query_evil_state", "craft_item"]
    assert out[1]["args"]["location_id"] == "edgewood_square"
    assert out[3]["args"] == {}
    assert out[4]["args"]["recipe_id"] == "herb_poultice"


def test_parse_normalizes_tool_calls():
    raw = '{"narration": "n", "choices": [], "tool_calls": [{"skill": "roll_dice", "arguments": {"sides": 20}}]}'
    out = parse_storyteller_response(raw)
    assert out["tool_calls"][0]["name"] == "roll_dice"
    assert out["tool_calls"][0]["args"]["sides"] == 20
