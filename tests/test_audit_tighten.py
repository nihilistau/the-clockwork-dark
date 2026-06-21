"""
Audit-tighten regression tests
==============================

Locks the fixes from the full review/audit pass:
  * the Assistant now shares the Storyteller's robust JSON extractor;
  * ``to_dict``/``from_dict`` round-trip the agent minds symmetrically;
  * a real save_game -> load_game disk round-trip preserves the newest fields;
  * AI-supplied challenge specs are size-bounded;
  * the localhost-by-default / upload-cap security posture.
"""

from __future__ import annotations

from pathlib import Path

from engine.agents.assistant import parse_assistant_response
from engine.config import get_config
from engine.game.challenges import start_challenge
from engine.game.procgen import new_game_state
from engine.game.saves import load_game, save_game
from engine.game.state import GameState


# --- Assistant robust parser (shares engine/agents/parsing.py) -------------

def test_assistant_parse_handles_nested_tool_args():
    # The old non-greedy regex truncated at the first '}', dropping the call.
    raw = (
        "The cat blinks once.\n"
        "```json\n"
        '{"text": "Mind the south field.", '
        '"tool_calls": [{"name": "assistant_gift", '
        '"args": {"item": {"id": "ward", "qty": 1}}}], '
        '"voice_style": "whisper"}\n'
        "```"
    )
    out = parse_assistant_response(raw)
    assert out["text"] == "Mind the south field."
    assert out["voice_style"] == "whisper"
    assert out["tool_calls"] == [
        {"name": "assistant_gift", "args": {"item": {"id": "ward", "qty": 1}}}
    ]


def test_assistant_parse_repairs_trailing_comma_and_falls_back_to_prose():
    # Trailing comma would break strict json.loads; no "text" key -> prose fallback.
    raw = 'A grey wanderer nods.\n```json\n{"voice_style": "dry", "tool_calls": [],}\n```'
    out = parse_assistant_response(raw)
    assert out["voice_style"] == "dry"
    assert out["tool_calls"] == []
    assert "grey wanderer" in out["text"]


def test_assistant_parse_plain_prose():
    out = parse_assistant_response("Just a quiet line, no json at all.")
    assert out["text"] == "Just a quiet line, no json at all."
    assert out["tool_calls"] == []
    assert out["voice_style"] == ""


# --- to_dict / from_dict symmetry + client redaction ----------------------

def test_to_dict_minds_symmetry_and_client_redaction():
    s = new_game_state(player_name="Mira", seed=3)
    s.storyteller_mind.patience = 12.5
    s.storyteller_mind.cruelty_bias = 0.9
    s.assistant_mind.trust_level = 77.0
    s.assistant_mind.current_form = "tinker"

    # Default payload is client-safe: no GM minds, no hidden fields.
    client = s.to_dict()
    assert "storyteller_mind" not in client
    assert "assistant_mind" not in client
    assert "awareness" not in client and "evil_progress" not in client

    # include_minds makes to_dict/from_dict a symmetric round-trip.
    full = s.to_dict(include_hidden=True, include_minds=True)
    restored = GameState.from_dict(full)
    assert restored.storyteller_mind.patience == 12.5
    assert restored.storyteller_mind.cruelty_bias == 0.9
    assert restored.assistant_mind.trust_level == 77.0
    assert restored.assistant_mind.current_form == "tinker"


# --- save_game -> load_game disk round-trip of the newest fields ----------

def test_save_round_trip_preserves_new_fields(tmp_path, monkeypatch):
    cfg = get_config()
    monkeypatch.setitem(cfg._data.setdefault("paths", {}), "saves", str(tmp_path))

    s = new_game_state(player_name="Bram", seed=11)
    s.engagement = 3.5
    s.evil_progress = 0.42
    s.awareness = 0.6
    s.doom_beats_seen = ["harvest_south", "scarecrow_wakes"]
    s.contracts = [
        {"id": "still_harvester", "title": "Still the South Harvester",
         "kind": "anti_dark", "status": "accepted"}
    ]
    s.challenge = {
        "id": "g1", "kind": "skill_gauntlet", "title": "The Lock",
        "steps": [{"skill": "nerve", "dc": 12, "text": "Pick it"}],
        "step": 0, "reward": {}, "fail": {},
    }
    s.combat = {"active": True, "enemy_id": "scarecrow", "enemy_hp": 8}
    s.assistant_mind.trust_level = 64.0

    save_game(s, label="rt")
    loaded = load_game(s.session_id)

    assert loaded.engagement == 3.5
    assert round(loaded.evil_progress, 3) == 0.42
    assert loaded.awareness == 0.6
    assert loaded.doom_beats_seen == ["harvest_south", "scarecrow_wakes"]
    assert loaded.contracts[0]["id"] == "still_harvester"
    assert loaded.challenge["kind"] == "skill_gauntlet"
    assert loaded.combat["enemy_id"] == "scarecrow"
    assert loaded.assistant_mind.trust_level == 64.0


# --- AI-supplied challenge spec size bounds -------------------------------

def test_challenge_spec_caps_reject_oversized():
    s = new_game_state(seed=1)

    big_steps = {"kind": "skill_gauntlet",
                 "steps": [{"skill": "nerve", "dc": 5, "text": "t"}] * 50}
    assert start_challenge(s, big_steps).status == "error"
    assert s.challenge is None  # rejected before storage

    big_nodes = {"kind": "decision_tree", "start": "n0",
                 "nodes": {f"n{i}": {"text": "t", "options": []} for i in range(60)}}
    assert start_challenge(s, big_nodes).status == "error"

    big_outcomes = {"kind": "dice_table",
                    "outcomes": [{"range": [1, 1], "result": {}}] * 40}
    assert start_challenge(s, big_outcomes).status == "error"


def test_challenge_puzzle_attempts_clamped():
    s = new_game_state(seed=1)
    r = start_challenge(s, {"kind": "puzzle", "answer": "key", "attempts": 999})
    assert r.status == "active"
    assert s.challenge["attempts_left"] == 12  # _MAX_ATTEMPTS


# --- security posture defaults -------------------------------------------

def test_config_security_defaults():
    cfg = get_config()
    assert cfg.get("scene.clockwork.host") == "127.0.0.1"
    origins = cfg.get("security.cors_origins")
    assert isinstance(origins, list) and origins
    assert all(("localhost" in o or "127.0.0.1" in o) for o in origins)
    assert float(cfg.get("security.max_upload_mb")) > 0


def test_flask_scene_sets_upload_cap():
    from engine.scenes.flask_scene import FlaskScene

    scene = FlaskScene(
        name="audit_probe",
        static_folder=Path("."),
        template_folder=Path("."),
        testing=True,
    )
    assert scene.app.config["MAX_CONTENT_LENGTH"] > 0
