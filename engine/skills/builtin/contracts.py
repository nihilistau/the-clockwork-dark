"""
Contract Skills (v0.6)
======================

Notice-board and character contracts — list / accept / complete. Rewards are
engine-authoritative; the Storyteller narrates the work and calls
``complete_contract`` when the objective is genuinely met.
"""

from __future__ import annotations

import json

from engine.game.contracts import ContractBoard
from engine.game.engine import get_active_engine
from engine.skills.registry import skill


@skill(
    pack="clockwork",
    description="List contracts offered at the player's current location (notice board / characters).",
    category="GAME",
    trigger="optional",
)
def list_contracts() -> str:
    """Available contracts here & now."""
    engine = get_active_engine()
    return json.dumps({"available": ContractBoard.available(engine.state)})


@skill(
    pack="clockwork",
    description="Accept a contract by id (adds it to the player's slate).",
    category="GAME",
    trigger="optional",
)
def accept_contract(contract_id: str) -> str:
    """Take on a contract."""
    engine = get_active_engine()
    return json.dumps(ContractBoard.accept(engine.state, contract_id))


@skill(
    pack="clockwork",
    description="Complete an accepted contract once its objective is genuinely met; engine grants the reward.",
    category="GAME",
    trigger="optional",
)
def complete_contract(contract_id: str) -> str:
    """Settle a contract and grant its reward."""
    engine = get_active_engine()
    return json.dumps(ContractBoard.complete(engine.state, contract_id))
