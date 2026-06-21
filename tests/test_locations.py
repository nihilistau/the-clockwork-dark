"""Location graph tests."""

from __future__ import annotations

from engine.game.engine import GameEngine
from engine.game.locations import CANONICAL_LOCATION_IDS, can_travel
from engine.game.state import GameState


def test_canonical_ids():
    assert "forest_clearing" in CANONICAL_LOCATION_IDS
    assert "edgewood_square" in CANONICAL_LOCATION_IDS
    assert "clockwork_tower" in CANONICAL_LOCATION_IDS
    assert len(CANONICAL_LOCATION_IDS) >= 12


def test_valid_travel():
    assert can_travel("forest_clearing", "edgewood_square")
    assert not can_travel("forest_clearing", "millhaven_gate")


def test_move_to_rejects_invalid():
    state = GameState(location_id="forest_clearing")
    engine = GameEngine(state)
    result = engine.move_to("millhaven_gate")
    assert result.success is False