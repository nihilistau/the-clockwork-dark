"""
Plot Formula
============

Computes plot_involvement and story_pressure from engine state.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

from engine.game.locations import LOCATIONS
from engine.game.state import GameState


class PlotFormula:
    """Derive narrative pressure signals from hard state."""

    @staticmethod
    def inward_distance(location_id: str) -> int:
        """Return location ring as proxy for distance to Heartlands."""
        loc = LOCATIONS.get(location_id, {})
        return int(loc.get("ring", 0))

    @staticmethod
    def compute(state: GameState) -> float:
        """
        Compute plot_involvement (0–100) from awareness, travel, and flags.

        Args:
            state: Current game state.

        Returns:
            Updated plot_involvement (also written to state).
        """
        ring = PlotFormula.inward_distance(state.location_id)
        main_quest_bonus = 15.0 if state.flags.get("main_quest_started") else 0.0
        involvement = (
            state.awareness * 0.4
            + ring * 12.0
            + main_quest_bonus
            + state.evil_progress * 20.0
        )
        state.plot_involvement = min(100.0, max(0.0, involvement))
        return state.plot_involvement

    @staticmethod
    def update_story_pressure(state: GameState) -> float:
        """
        Story pressure rises with plot involvement and low storyteller patience.

        Args:
            state: Current game state.

        Returns:
            story_pressure 0–100.
        """
        PlotFormula.compute(state)
        patience_factor = (100.0 - state.storyteller_mind.patience) * 0.3
        pressure = state.plot_involvement * 0.7 + patience_factor
        state.story_pressure = min(100.0, max(0.0, pressure))
        return state.story_pressure