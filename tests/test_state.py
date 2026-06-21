"""GameState serialization tests."""

from __future__ import annotations

from engine.game.state import EvilPhase, GameState, InventoryItem


def test_round_trip():
    state = GameState(
        player_name="Alden",
        location_id="edgewood_square",
        awareness=12.5,
        evil_progress=0.25,
        story_pressure=30.0,
        inventory=[InventoryItem(id="loaf", name="Loaf", qty=2)],
    )
    data = state.to_dict(include_hidden=True)
    restored = GameState.from_dict({**data, "awareness": 12.5, "evil_progress": 0.25})
    assert restored.player_name == "Alden"
    assert restored.location_id == "edgewood_square"
    assert restored.evil_phase == EvilPhase.STIRRING
    assert restored.inventory[0].qty == 2