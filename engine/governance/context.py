"""
TurnContext (PR19)
==================

Mutable carrier threaded through the governance pipeline. PRE hooks shape the
prompt; POST hooks audit the resolved turn. Interceptors may set ``abort`` to
short-circuit the remaining chain.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engine.game.state import GameState


@dataclass
class TurnContext:
    """State carried through one agent turn's governance pipeline."""

    state: GameState
    player_action: str = ""
    agent: str = "storyteller"
    system_prompt: str = ""
    raw: str = ""
    parsed: dict[str, Any] = field(default_factory=dict)
    narration: str = ""
    tool_receipts: list[dict[str, Any]] = field(default_factory=list)
    processed_tags: dict[str, list[str]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    violations: list[dict[str, Any]] = field(default_factory=list)
    abort: bool = False
    skip_llm: bool = False

    def add_violation(self, rule_id: str, message: str, severity: str = "error") -> None:
        self.violations.append(
            {"rule_id": rule_id, "message": message, "severity": severity}
        )
