"""
Game Saves
==========

JSON save/load for session state.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from engine.config import get_config
from engine.game.state import GameState

logger = logging.getLogger(__name__)

_ROOT = Path(__file__).resolve().parents[2]


def saves_dir() -> Path:
    """Resolved saves directory."""
    rel = get_config().get("paths.saves", "data/saves")
    path = _ROOT / rel
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_path(session_id: str) -> Path:
    """Path for a session save file."""
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_")
    return saves_dir() / f"{safe}.json"


def save_game(state: GameState, *, label: str = "") -> dict[str, Any]:
    """
    Persist game state to disk.

    Returns:
        Metadata dict with path and saved_at.
    """
    payload = state.to_dict(include_hidden=True)
    payload["storyteller_mind"] = {
        k: getattr(state.storyteller_mind, k)
        for k in state.storyteller_mind.__dataclass_fields__
    }
    payload["assistant_mind"] = {
        k: getattr(state.assistant_mind, k)
        for k in state.assistant_mind.__dataclass_fields__
    }
    payload["save_label"] = label or state.player_name
    payload["saved_at"] = datetime.now(timezone.utc).isoformat()

    path = save_path(state.session_id)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    logger.info("[saves] Game saved (operation=save, path=%s)", path)
    return {"path": str(path), "session_id": state.session_id, "saved_at": payload["saved_at"]}


def load_game(session_id: str) -> GameState:
    """Load game state from disk by session id."""
    path = save_path(session_id)
    if not path.exists():
        raise FileNotFoundError(f"No save for session {session_id}")
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    return GameState.from_dict(data)


def list_saves() -> list[dict[str, Any]]:
    """List available save files with metadata."""
    entries: list[dict[str, Any]] = []
    for path in sorted(saves_dir().glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            with path.open(encoding="utf-8") as fh:
                data = json.load(fh)
            entries.append({
                "session_id": data.get("session_id", path.stem),
                "player_name": data.get("player_name", ""),
                "location_id": data.get("location_id", ""),
                "world_day": data.get("world_day", 1),
                "saved_at": data.get("saved_at", ""),
                "path": str(path),
            })
        except (json.JSONDecodeError, OSError):
            continue
    return entries