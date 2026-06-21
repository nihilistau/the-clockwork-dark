"""
Cutscene Milestones (v0.2, PR15)
================================

Fires one-shot milestone cutscenes as the story escalates:

  * the world entering **STIRRING**      → ``cutscene_stirring_phase``
  * the Assistant's **reveal**            → ``cutscene_assistant_reveal``
  * the **Consuming Horizon**             → ``cutscene_consuming_horizon``

Each fires at most once per session (tracked via ``state.flags``) and is subject
to the phase-shift cutscene budget. If the budget blocks a due milestone, its
flag is left unset so it retries on the next phase shift.

Version: v0.2.0 [2026-06-21]
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable, Optional

from engine.config import get_config
from engine.game.state import GameState
from engine.media.cutscene import CutsceneRunner
from engine.media.queue import MediaJob

logger = logging.getLogger(__name__)


def _phase_idx(phase: str) -> int:
    from engine.game.evil_ticker import phase_index

    return phase_index(phase)


@dataclass
class Milestone:
    flag: str
    cutscene_id: str
    condition: Callable[[GameState], bool]


def _milestones() -> list[Milestone]:
    reveal_min = float(get_config().get("awareness.reflection_form_min", 40))
    return [
        Milestone(
            "milestone_stirring",
            "cutscene_stirring_phase",
            lambda s: _phase_idx(s.evil_phase.value) >= _phase_idx("stirring"),
        ),
        Milestone(
            "milestone_assistant_reveal",
            "cutscene_assistant_reveal",
            lambda s: bool(s.flags.get("assistant_revealed")) or s.awareness >= reveal_min,
        ),
        Milestone(
            "milestone_consuming",
            "cutscene_consuming_horizon",
            lambda s: _phase_idx(s.evil_phase.value) >= _phase_idx("consuming"),
        ),
    ]


class CutsceneMilestones:
    """Detect and fire story-milestone cutscenes (phase-shift budgeted)."""

    @staticmethod
    def due_milestone(state: GameState) -> Optional[Milestone]:
        """Return the first unfired milestone whose condition is satisfied."""
        for m in _milestones():
            if not state.flags.get(m.flag) and m.condition(state):
                return m
        return None

    @staticmethod
    def trigger(
        state: GameState,
        *,
        runner: Optional[CutsceneRunner] = None,
        force: bool = False,
    ) -> Optional[MediaJob]:
        """Enqueue the next due milestone cutscene, if the budget allows.

        Returns the enqueued :class:`MediaJob`, or ``None`` if nothing is due or
        the budget blocked it. The milestone flag is only set once the cutscene
        actually enqueues, so a budget-blocked milestone retries later.
        """
        m = CutsceneMilestones.due_milestone(state)
        if m is None:
            return None
        runner = runner or CutsceneRunner()
        job = runner.enqueue_cutscene(m.cutscene_id, state, force=force)
        if job is None:
            return None
        state.flags[m.flag] = True
        logger.info(
            "[milestones] Fired (operation=trigger, milestone=%s, cutscene=%s)",
            m.flag,
            m.cutscene_id,
        )
        return job
