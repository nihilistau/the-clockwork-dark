"""
Assistant Director (PR27)
=========================

The signature "unreliable companion" engine. Each turn it decides — from trust,
the player's struggle, the evil phase, and how recently it last appeared —
*whether* the Assistant shows up, *with what* (a quip, a hint, lore, a warning,
or the right item at the right moment), and *how reliably* (low trust → its
advice may mislead). In calm moments it is simply indifferent.

Design contract: in a calm default state the appear-roll equals the legacy
``should_assistant_speak(help_probability)`` (one rng draw first), so existing
behavior is preserved; bonuses only kick in under struggle/drama.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Optional

from engine.config import get_config
from engine.game.state import GameState


def _phase_idx(phase: str) -> int:
    from engine.game.evil_ticker import phase_index

    return phase_index(phase)


@dataclass
class AssistantDecision:
    appear: bool
    intent: str = "silent"  # silent | quip | hint | lore | warning | gift
    reliability: float = 1.0
    reliable: bool = True
    gift_item: Optional[dict[str, str]] = None
    reason: str = ""
    score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "appear": self.appear,
            "intent": self.intent,
            "reliability": round(self.reliability, 3),
            "reliable": self.reliable,
            "gift_item": self.gift_item,
            "reason": self.reason,
            "score": round(self.score, 3),
        }


class AssistantDirector:
    """Decides whether/how the Assistant intervenes this turn."""

    GIFT_COOLDOWN = 5  # turns between unsolicited gifts

    def decide(
        self,
        state: GameState,
        *,
        context: str = "",
        rng: Optional[random.Random] = None,
    ) -> AssistantDecision:
        rng = rng or random.Random()
        mind = state.assistant_mind
        base = float(mind.help_probability)
        trust = max(0.0, min(1.0, mind.trust_level / 100.0))

        struggle = self._struggle(state)
        drama = self._drama(state)
        cooldown = 0.3 if self._recent_appearance(state) else 0.0

        score = base + struggle + drama - cooldown
        # The "right moment" floor — at real danger it tends to show up.
        if struggle >= 0.85:
            score = max(score, 0.9)
        score = max(0.0, min(1.0, score))

        # --- appear roll FIRST (matches legacy single-draw behavior) ---
        if rng.random() > score:
            return AssistantDecision(
                appear=False, intent="silent", score=score, reason="indifferent"
            )

        reliability = max(0.0, min(1.0, 0.45 + 0.5 * trust))
        reliable = rng.random() <= reliability

        intent, gift = self._intent(state, trust, struggle, drama, rng)
        return AssistantDecision(
            appear=True,
            intent=intent,
            reliability=reliability,
            reliable=reliable,
            gift_item=gift,
            score=score,
            reason=intent,
        )

    # --- signals ---------------------------------------------------------
    @staticmethod
    def _struggle(state: GameState) -> float:
        s = 0.0
        if state.combat is not None:
            s = max(s, 0.4)
        hp_frac = state.stats.hp / max(1, state.stats.max_hp)
        if hp_frac < 0.4:
            s = max(s, 0.6)
        if hp_frac < 0.2:
            s = max(s, 0.85)
        if state.flags.get("combat_defeat"):
            s = max(s, 0.5)
        if state.stats.stamina < 15:
            s = max(s, 0.4)
        return s

    @staticmethod
    def _drama(state: GameState) -> float:
        d = 0.15 * _phase_idx(state.evil_phase.value)
        if state.flags.get("assistant_dramatic_beat"):
            d = max(d, 0.4)
        return d

    def _recent_appearance(self, state: GameState) -> bool:
        last = state.flags.get("_assistant_last_turn")
        return isinstance(last, int) and (state.turn_number - last) < 2

    def _intent(
        self,
        state: GameState,
        trust: float,
        struggle: float,
        drama: float,
        rng: random.Random,
    ) -> tuple[str, Optional[dict[str, str]]]:
        if struggle >= 0.4:
            if trust >= 0.3 and not self._gifted_recently(state) and rng.random() <= 0.5:
                gift = self._pick_gift(state)
                if gift:
                    return "gift", gift
            return "hint", None
        reflection_min = float(get_config().get("awareness.reflection_form_min", 40))
        if state.awareness >= reflection_min:
            return "lore", None
        if drama >= 0.3:
            return "warning", None
        return "quip", None

    def _gifted_recently(self, state: GameState) -> bool:
        last = state.flags.get("_assistant_gift_turn")
        return isinstance(last, int) and (state.turn_number - last) < self.GIFT_COOLDOWN

    @staticmethod
    def _pick_gift(state: GameState) -> Optional[dict[str, str]]:
        hp_frac = state.stats.hp / max(1, state.stats.max_hp)
        fear = int((state.combat or {}).get("fear", 0))
        if hp_frac < 0.5:
            return {"id": "bandage_poultice", "name": "Bandage Poultice"}
        if fear >= 4:
            return {"id": "ward_charm", "name": "Warding Charm"}
        if state.stats.stamina < 30:
            return {"id": "forest_tonic", "name": "Forest Tonic"}
        return None
