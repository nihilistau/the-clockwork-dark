"""
Notice Board & Contracts (PR-contracts, v0.6)
=============================================

Opt-in missions — the connective tissue of the "puzzle you experience, not a
quest thrust on you" design. The player may take none and bake bread, or pick up
bounties against the Dark from the town notice board or from characters. Rewards
are engine-authoritative; the Storyteller narrates the work (often as combat or
an ephemeral [[ephemeral-challenges]] challenge) and calls ``complete_contract``
when the objective is genuinely met.

Contracts are defined in ``data/contracts.yaml``; accepted ones live on
``GameState.contracts``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml

from engine.config import get_config
from engine.game.evil_ticker import phase_index
from engine.game.state import GameState, InventoryItem

_ROOT = Path(__file__).resolve().parents[2]
_CACHE: Optional[dict[str, Any]] = None


def load_contracts() -> dict[str, Any]:
    """Load + cache the contract catalogue."""
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    rel = get_config().get("paths.contracts", "data/contracts.yaml")
    path = _ROOT / rel
    if not path.exists():
        _CACHE = {}
        return _CACHE
    with path.open(encoding="utf-8") as fh:
        _CACHE = yaml.safe_load(fh) or {}
    return _CACHE


def reset_contracts_cache() -> None:
    global _CACHE
    _CACHE = None


def _taken_ids(state: GameState) -> set[str]:
    return {c.get("id") for c in state.contracts}


def _gate_ok(state: GameState, spec: dict[str, Any]) -> bool:
    min_phase = str(spec.get("min_phase", "dormant"))
    if phase_index(state.evil_phase.value) < phase_index(min_phase):
        return False
    if state.awareness < float(spec.get("min_awareness", 0)):
        return False
    return True


class ContractBoard:
    """List / accept / complete notice-board and character contracts."""

    @staticmethod
    def available(state: GameState) -> list[dict[str, Any]]:
        """Contracts offered at the player's current location, not yet taken."""
        taken = _taken_ids(state)
        out: list[dict[str, Any]] = []
        for cid, spec in load_contracts().items():
            if cid in taken:
                continue
            if spec.get("location") and spec["location"] != state.location_id:
                continue
            if not _gate_ok(state, spec):
                continue
            out.append({
                "id": cid,
                "title": spec.get("title", cid),
                "giver": spec.get("giver", "noticeboard"),
                "kind": spec.get("kind", "mundane"),
                "summary": spec.get("summary", ""),
            })
        return out

    @staticmethod
    def accept(state: GameState, contract_id: str) -> dict[str, Any]:
        catalogue = load_contracts()
        spec = catalogue.get(contract_id)
        if spec is None:
            return {"success": False, "message": f"No such contract: {contract_id}."}
        if contract_id in _taken_ids(state):
            return {"success": False, "message": "Already on your slate."}
        if not _gate_ok(state, spec):
            return {"success": False, "message": "That posting isn't open to you yet."}
        state.contracts.append({
            "id": contract_id,
            "title": spec.get("title", contract_id),
            "kind": spec.get("kind", "mundane"),
            "status": "accepted",
        })
        return {"success": True, "contract_id": contract_id, "status": "accepted"}

    @staticmethod
    def complete(state: GameState, contract_id: str) -> dict[str, Any]:
        entry = next((c for c in state.contracts if c.get("id") == contract_id), None)
        if entry is None:
            return {"success": False, "message": "You haven't taken that contract."}
        if entry.get("status") == "complete":
            return {"success": False, "message": "Already settled."}
        spec = load_contracts().get(contract_id, {})
        applied = ContractBoard._apply_reward(state, spec.get("reward", {}))
        entry["status"] = "complete"
        return {"success": True, "contract_id": contract_id, "status": "complete", "reward": applied}

    @staticmethod
    def active(state: GameState) -> list[dict[str, Any]]:
        return [c for c in state.contracts if c.get("status") != "complete"]

    @staticmethod
    def _apply_reward(state: GameState, reward: dict[str, Any]) -> dict[str, Any]:
        applied: dict[str, Any] = {}
        if not isinstance(reward, dict):
            return applied
        if "gold" in reward:
            state.stats.gold += int(reward["gold"])
            applied["gold"] = state.stats.gold
        if "engagement" in reward:
            from engine.game.doom_clock import DoomClock

            applied["engagement"] = DoomClock.register_engagement(state, float(reward["engagement"]))
        if "awareness" in reward:
            state.awareness = max(0.0, min(100.0, state.awareness + float(reward["awareness"])))
            applied["awareness"] = state.awareness
        if "hp" in reward:
            state.stats.hp = max(0, min(state.stats.max_hp, state.stats.hp + int(reward["hp"])))
            applied["hp"] = state.stats.hp
        if "item" in reward and isinstance(reward["item"], dict):
            it = reward["item"]
            _add_item(state, str(it.get("id", "")), str(it.get("name", "")))
            applied["item"] = it
        if "reputation" in reward and isinstance(reward["reputation"], dict):
            for npc, amt in reward["reputation"].items():
                state.reputations[npc] = state.reputations.get(npc, 0) + int(amt)
            applied["reputation"] = dict(reward["reputation"])
        return applied


def _add_item(state: GameState, item_id: str, name: str) -> None:
    if not item_id:
        return
    for entry in state.inventory:
        if entry.id == item_id:
            entry.qty += 1
            return
    state.inventory.append(InventoryItem(id=item_id, name=name or item_id, qty=1, tags=["contract"]))
