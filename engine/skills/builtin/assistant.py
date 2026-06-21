"""
Assistant Skills
================

Optional narrative tools for clockwork_assistant.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import json
from typing import Any

from engine.config import get_config
from engine.game.engine import get_active_engine
from engine.skills.registry import TRIGGER_OPTIONAL, skill

ASSISTANT_FORMS: tuple[str, ...] = (
    "cat",
    "wanderer",
    "child",
    "tinker",
    "reflection",
)

HINTS_BY_TIER: dict[int, list[str]] = {
    1: [
        "The smoke from Edgewood drifts west, even when the wind blows south.",
        "Brindle the cat watches the road longer than any cat should.",
    ],
    2: [
        "Maris hums while kneading — villagers say it keeps the gears quiet.",
        "Tinkers sell ward-charms before the wheat turns wrong.",
    ],
    3: [
        "Something in the wheat remembers being wound. Avoid bread with brass flecks.",
        "The broken village clock still ticks, but not with any hour you know.",
    ],
}

LORE_SNIPPETS: dict[str, dict[str, Any]] = {
    "edgewood": {
        "min_tier": 1,
        "text": (
            "Edgewood is the last comfortable village before the Marches — "
            "timber frames, a communal oven, and a shrine to saints nobody names."
        ),
    },
    "grey_wanderer": {
        "min_tier": 2,
        "text": (
            "Folklore calls them the Grey Wanderer: a hooded figure who asks "
            "questions and never answers yours."
        ),
    },
    "clockwork_dark": {
        "min_tier": 3,
        "text": (
            "The Clockwork Dark is not a plague but a winding — brass teeth "
            "in stillborn lambs, gears in grain, time eating the land from within."
        ),
    },
}


def compute_hint_tier(trust_level: float, plot_involvement: float) -> int:
    """
    Derive hint tier from trust and plot involvement (no evil_progress).

    Args:
        trust_level: Assistant trust 0–100.
        plot_involvement: Player plot involvement 0–100.

    Returns:
        Hint tier 1–3.
    """
    tier = 1
    if trust_level >= 30.0:
        tier = 2
    if trust_level >= 60.0 or plot_involvement >= 20.0:
        tier = 3
    return max(1, min(3, tier))


def _reflection_min_awareness() -> float:
    return float(
        get_config().get(
            "assistant.reflection_awareness_min",
            get_config().get("awareness.reflection_form_min", 40),
        )
    )


@skill(
    pack="clockwork",
    description="Assistant: return a lore hint appropriate to trust tier.",
    category="NARRATIVE",
    trigger=TRIGGER_OPTIONAL,
)
def grant_hint(tier: int = 0) -> str:
    """Return hint text capped by computed hint tier."""
    engine = get_active_engine()
    state = engine.state
    max_tier = compute_hint_tier(
        state.assistant_mind.trust_level,
        state.plot_involvement,
    )
    effective = tier if tier > 0 else max_tier
    effective = max(1, min(effective, max_tier))
    pool = HINTS_BY_TIER.get(effective, HINTS_BY_TIER[1])
    idx = state.turn_number % len(pool)
    return json.dumps(
        {
            "tier": effective,
            "max_tier": max_tier,
            "hint": pool[idx],
        }
    )


@skill(
    pack="clockwork",
    description="Assistant: reveal a lore snippet by topic id.",
    category="NARRATIVE",
    trigger=TRIGGER_OPTIONAL,
)
def reveal_lore(topic: str = "edgewood") -> str:
    """Return lore snippet if hint tier permits."""
    engine = get_active_engine()
    state = engine.state
    max_tier = compute_hint_tier(
        state.assistant_mind.trust_level,
        state.plot_involvement,
    )
    entry = LORE_SNIPPETS.get(topic.lower())
    if entry is None:
        return json.dumps(
            {
                "success": False,
                "topic": topic,
                "message": f"Unknown lore topic: {topic}",
            }
        )
    min_tier = int(entry.get("min_tier", 1))
    if max_tier < min_tier:
        return json.dumps(
            {
                "success": False,
                "topic": topic,
                "required_tier": min_tier,
                "max_tier": max_tier,
                "message": "Trust is not deep enough for that truth.",
            }
        )
    return json.dumps(
        {
            "success": True,
            "topic": topic,
            "tier": max_tier,
            "lore": entry["text"],
        }
    )


@skill(
    pack="clockwork",
    description="Assistant: shift visible form (cat, wanderer, child, tinker, reflection).",
    category="NARRATIVE",
    trigger=TRIGGER_OPTIONAL,
)
def change_form(form: str) -> str:
    """Change assistant_mind.current_form with awareness gate on reflection."""
    engine = get_active_engine()
    state = engine.state
    target = form.lower().strip()
    if target not in ASSISTANT_FORMS:
        return json.dumps(
            {
                "success": False,
                "form": target,
                "message": f"Unknown form: {target}",
                "valid_forms": list(ASSISTANT_FORMS),
            }
        )
    if target == "reflection" and state.awareness < _reflection_min_awareness():
        return json.dumps(
            {
                "success": False,
                "form": target,
                "required_awareness": _reflection_min_awareness(),
                "awareness": state.awareness,
                "message": "The reflection will not hold yet.",
            }
        )
    previous = state.assistant_mind.current_form
    state.assistant_mind.current_form = target
    return json.dumps(
        {
            "success": True,
            "previous_form": previous,
            "form": target,
        }
    )