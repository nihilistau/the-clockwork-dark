"""
Evil Ticker
===========

Background evil progression — always advances.

Units: evil_progress is 0.0–1.0 (dimensionless).
evil_base_rate_per_day from config is added per in-game day elapsed.

Phase boundaries (inclusive lower, exclusive upper):
  DORMANT:   [0.0, 0.2)
  STIRRING:  [0.2, 0.5)
  SPREADING: [0.5, 0.8)
  CONSUMING: [0.8, 1.0]

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

from engine.config import get_config
from engine.game.locations import evil_multiplier_for
from engine.game.state import EvilPhase, GameState

PHASE_THRESHOLDS: list[tuple[float, EvilPhase]] = [
    (0.0, EvilPhase.DORMANT),
    (0.2, EvilPhase.STIRRING),
    (0.5, EvilPhase.SPREADING),
    (0.8, EvilPhase.CONSUMING),
]


_PHASE_INDEX: dict[str, int] = {
    EvilPhase.DORMANT.value: 0,
    EvilPhase.STIRRING.value: 1,
    EvilPhase.SPREADING.value: 2,
    EvilPhase.CONSUMING.value: 3,
}


def phase_index(phase: str) -> int:
    """Return ordinal index for phase comparison."""
    return _PHASE_INDEX.get(phase, 0)


def phase_from_progress(progress: float) -> EvilPhase:
    """Map progress to phase using inclusive lower bounds."""
    clamped = max(0.0, min(1.0, progress))
    result = EvilPhase.DORMANT
    for threshold, phase in PHASE_THRESHOLDS:
        if clamped >= threshold:
            result = phase
    return result


class EvilTicker:
    """Advances evil_progress based on world time and location."""

    @staticmethod
    def base_rate_per_day() -> float:
        """Configured daily evil advance rate."""
        return float(get_config().get("world.evil_base_rate_per_day", 0.01))

    @staticmethod
    def advance(state: GameState, *, days_elapsed: float = 1.0) -> float:
        """
        Advance evil_progress and update evil_phase on state.

        Args:
            state: Mutable game state.
            days_elapsed: In-game days since last advance.

        Returns:
            New evil_progress value.
        """
        multiplier = evil_multiplier_for(state.location_id)
        inaction_bonus = 1.0 + max(0, state.world_day - state.turn_number) * 0.001
        # Engagement holds the Dark back: up to 40% slower when the player keeps
        # pushing. Default engagement 0.0 -> factor 1.0 (no change).
        engagement_factor = 1.0 - min(0.6, max(0.0, state.engagement) / 100.0) * 0.6
        delta = (
            EvilTicker.base_rate_per_day()
            * days_elapsed
            * multiplier
            * inaction_bonus
            * engagement_factor
        )
        state.evil_progress = min(1.0, state.evil_progress + delta)
        state.evil_phase = phase_from_progress(state.evil_progress)
        # Engagement decays so the player must keep confronting the Dark.
        if state.engagement > 0.0:
            state.engagement = max(0.0, state.engagement - 0.5 * days_elapsed)
        return state.evil_progress

    @staticmethod
    def snapshot(state: GameState) -> dict[str, str | float]:
        """Full evil snapshot for Storyteller tools."""
        return {
            "evil_progress": state.evil_progress,
            "evil_phase": state.evil_phase.value,
            "story_pressure": state.story_pressure,
            "plot_involvement": state.plot_involvement,
            "awareness": state.awareness,
        }