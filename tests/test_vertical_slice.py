"""
Vertical slice smoke test — PR12 acceptance criteria.

new_game → forest_clearing → edgewood_square → trade → caravan rumor → evil tick
"""

from __future__ import annotations

import json

import engine.skills.builtin.mechanics  # noqa: F401
from content.scenes.clockwork.clockwork_state import SessionStore, run_turn
from engine.game.engine import GameEngine, set_active_engine
from engine.game.locations import reload_locations
from engine.game.procgen import new_game_state
from engine.game.saves import load_game, save_game
from engine.skills.registry import SKILL_REGISTRY
from engine.world.world_sim import WorldSim

MOCK_STORYTELLER = """
```json
{
  "tool_calls": [],
  "narration": "Smoke threads the birch. Edgewood waits.",
  "choices": [{"id": "a", "text": "Walk toward the village"}],
  "tags_inline": "[IMAGE:forest_clearing_dawn]"
}
```
"""


def test_vertical_slice_flow():
    reload_locations()
    store = SessionStore()
    session = store.create(
        player_name="Traveler",
        archetype="wayfarer",
        seed=42,
        llm_fn=lambda _messages: MOCK_STORYTELLER,
    )
    state = session.engine.state

    assert state.location_id == "forest_clearing"

    set_active_engine(session.engine)
    move_raw = SKILL_REGISTRY.invoke("move_to", location_id="edgewood_square")
    move = json.loads(move_raw)
    assert move["success"] is True
    assert state.location_id == "edgewood_square"

    state.location_id = "edgewood_bakery"
    state.stats.gold = 10
    trade_raw = SKILL_REGISTRY.invoke(
        "trade", action="buy", item_id="loaf", npc_id="npc_maris"
    )
    trade = json.loads(trade_raw)
    assert trade["success"] is True
    assert state.reputations.get("npc_maris", 0) >= 1

    tick = WorldSim.on_tick(state, days_elapsed=10.0, force=["caravan_arrival"])
    assert tick
    assert state.rumors or state.world_events

    before = state.evil_progress
    WorldSim.on_tick(state, days_elapsed=5.0)
    assert state.evil_progress >= before

    turn = run_turn(session, "Look around the square.")
    assert turn.get("narration")
    assert turn.get("scene", {}).get("location_id")
    assert "overlay" in turn.get("scene", {})


def test_save_load_round_trip(tmp_path, monkeypatch):
    from engine.config import get_config

    cfg = get_config()
    monkeypatch.setitem(cfg._data.setdefault("paths", {}), "saves", str(tmp_path))

    state = new_game_state(seed=99)
    state.location_id = "edgewood_square"
    save_game(state)

    loaded = load_game(state.session_id)
    assert loaded.location_id == "edgewood_square"
    assert loaded.procgen.seed == state.procgen.seed