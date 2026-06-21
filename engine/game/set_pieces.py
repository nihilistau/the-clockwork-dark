"""
Set-pieces — authored, discoverable challenges
==============================================

A *set-piece* is a hand-authored ephemeral challenge ([[ephemeral-challenges]])
keyed by id in ``data/set_pieces.yaml`` — a discovery the player *experiences*
(the tunnel-mouth descent, a barrow's reckoning) rather than one the Storyteller
improvises. The engine still owns the outcome: a set-piece is just a stored
``start_challenge`` spec, gated on the world having reached it.

Gates use the same world-reactive flags the Doom Clock sets ([[the-reactive-world]]):
``requires_flag`` / ``requires_discovery`` keep a set-piece sealed until its
ground has actually opened — you cannot descend a tunnel that has not yet been
unsealed. The spec is otherwise a normal challenge (decision_tree / puzzle /
skill_gauntlet / dice_table); ``resolve_challenge`` drives it from there.
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any, Optional

import yaml

from engine.config import get_config
from engine.game.challenges import ChallengeResult, start_challenge
from engine.game.state import GameState

_ROOT = Path(__file__).resolve().parents[2]
_CACHE: Optional[dict[str, Any]] = None


def load_set_pieces() -> dict[str, Any]:
    """Load + cache the authored set-piece library."""
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    rel = get_config().get("paths.set_pieces", "data/set_pieces.yaml")
    path = _ROOT / rel
    if not path.exists():
        _CACHE = {}
        return _CACHE
    with path.open(encoding="utf-8") as fh:
        _CACHE = yaml.safe_load(fh) or {}
    return _CACHE


def reset_set_pieces_cache() -> None:
    global _CACHE
    _CACHE = None


def _gate_ok(state: GameState, spec: dict[str, Any]) -> tuple[bool, str]:
    """A set-piece is sealed until the world has opened its ground."""
    req_flag = spec.get("requires_flag")
    if req_flag and not state.flags.get(req_flag):
        return False, "There is nothing here to descend into — not yet."
    req_disc = spec.get("requires_discovery")
    if req_disc and not state.flags.get(f"discovery_{req_disc}"):
        return False, "The way is not open."
    return True, ""


def start_set_piece(
    state: GameState,
    set_piece_id: str,
    *,
    rng: Optional[random.Random] = None,
) -> ChallengeResult:
    """Present an authored set-piece as an active challenge, if the world has
    reached it. Delegates resolution to the standard challenge engine."""
    spec = load_set_pieces().get(set_piece_id)
    if not isinstance(spec, dict):
        return ChallengeResult("", "set_piece", "error", message=f"No set-piece: {set_piece_id}.", ended=True)
    ok, reason = _gate_ok(state, spec)
    if not ok:
        return ChallengeResult(set_piece_id, str(spec.get("kind", "")), "error", message=reason, ended=True)
    challenge_spec = {k: v for k, v in spec.items()
                      if k not in ("requires_flag", "requires_discovery")}
    challenge_spec.setdefault("id", set_piece_id)
    return start_challenge(state, challenge_spec, rng=rng)
