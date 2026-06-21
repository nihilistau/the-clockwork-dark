"""Save/load tests."""

from __future__ import annotations

from engine.game.procgen import new_game_state
from engine.game.saves import list_saves, load_game, save_game


def test_save_and_list(tmp_path, monkeypatch):
    from engine.config import get_config

    cfg = get_config()
    monkeypatch.setitem(cfg._data.setdefault("paths", {}), "saves", str(tmp_path))

    state = new_game_state(player_name="Aldric", seed=7)
    meta = save_game(state, label="test")
    assert meta["session_id"] == state.session_id

    entries = list_saves()
    assert any(e["session_id"] == state.session_id for e in entries)

    loaded = load_game(state.session_id)
    assert loaded.player_name == "Aldric"