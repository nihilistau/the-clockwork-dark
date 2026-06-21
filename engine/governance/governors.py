"""
Builtin Governors / Interceptors (PR19)
=======================================

PRE shapers (EvilPhaseTone, StorytellerMind) and the POST RulesGovernor that
finally wires SceneRulesEngine (R001–R005) into every Storyteller turn. The
existing LoreInject/AwarenessGate PRE interceptors are registered by name so
``GovernancePipeline.from_config`` can resolve them from ``comms.interceptors``.
"""

from __future__ import annotations

import logging

from engine.governance.context import TurnContext
from engine.governance.pipeline import _PRE_REGISTRY, interceptor
from engine.lore.interceptors import AwarenessGateInterceptor, LoreInjectInterceptor
from engine.mcp.scene_rules_engine import get_rules_engine

logger = logging.getLogger(__name__)

# Existing PRE interceptors resolvable by config name.
_PRE_REGISTRY.setdefault("LoreInjectInterceptor", LoreInjectInterceptor)
_PRE_REGISTRY.setdefault("AwarenessGateInterceptor", AwarenessGateInterceptor)


@interceptor("pre", priority=20)
class EvilPhaseTone:
    """PRE: nudge narration tone toward the current evil phase (no spoilers)."""

    _TONE = {
        "dormant": "Tone: cozy frontier life; the wrongness is barely a rumor.",
        "stirring": "Tone: small wrongnesses creep in — brass glints, odd silences.",
        "spreading": "Tone: dread thickens; the corruption is undeniable to the watchful.",
        "consuming": "Tone: stark, high-contrast horror; the world is coming apart.",
    }

    def run_pre(self, state, system_prompt, *, player_action="", **_):
        line = self._TONE.get(state.evil_phase.value)
        return f"{system_prompt}\n\n{line}" if line else system_prompt


@interceptor("pre", priority=15)
class DoomBeatInterceptor:
    """PRE: surface the Doom Clock's arc + latest world-sign so the Narrator lets
    the Dark advance as slow dread the player may notice or ignore."""

    def run_pre(self, state, system_prompt, *, player_action="", **_):
        from engine.game.doom_clock import DoomClock

        arc = DoomClock.arc(state)
        latest = DoomClock.latest_beat(state)
        lines = [f"WORLD STATE: doom arc = {arc}."]
        if latest is not None:
            lines.append(f"The Dark has already reached: {latest.text}")
        lines.append(
            "Let the corruption advance in the background as slow dread — present "
            "signs the player may notice or ignore. Do not resolve it for them; "
            "this is a world to experience, not a quest thrust upon them."
        )
        return f"{system_prompt}\n\n" + "\n".join(lines)


@interceptor("pre", priority=30)
class StorytellerMind:
    """PRE: translate the Storyteller agency knobs into GM directives."""

    def run_pre(self, state, system_prompt, *, player_action="", **_):
        m = state.storyteller_mind
        bits: list[str] = []
        if m.cruelty_bias >= 0.5:
            bits.append("lean harsher with consequences")
        elif m.cruelty_bias <= 0.2:
            bits.append("be merciful with consequences")
        if m.reward_generosity >= 0.6:
            bits.append("reward clever play generously")
        if m.patience <= 20:
            bits.append("the world grows impatient; raise the stakes")
        if not bits:
            return system_prompt
        return f"{system_prompt}\n\nGM disposition: " + "; ".join(bits) + "."


@interceptor("post", priority=50)
class RulesGovernor:
    """POST: audit a resolved turn against SceneRulesEngine (R001–R005)."""

    def run_post(self, ctx: TurnContext) -> TurnContext:
        from engine.game.locations import CANONICAL_LOCATION_IDS

        eng = get_rules_engine()
        state = ctx.state

        # R005 — awareness range (clamp + record any breach).
        ar = eng.validate_awareness(state.awareness)
        if not ar.allowed:
            for v in ar.violations:
                ctx.add_violation(v.rule_id, v.message, v.severity)
            state.awareness = max(0.0, min(100.0, state.awareness))

        # R004 — evil_progress must not decrease across the turn.
        evil_before = ctx.metadata.get("evil_before")
        if evil_before is not None:
            er = eng.validate_evil_progress(
                float(evil_before), float(state.evil_progress)
            )
            if not er.allowed:
                for v in er.violations:
                    ctx.add_violation(v.rule_id, v.message, v.severity)

        # R001 — the player must be at a canonical location.
        if state.location_id not in CANONICAL_LOCATION_IDS:
            ctx.add_violation("R001", f"Non-canonical location: {state.location_id}")

        # R003 — the LLM claimed stat deltas without a tool receipt. The engine
        # already ignored them (stats only change via skills); we record the
        # overreach for governance + telemetry.
        receipt_ctx = {"tool_receipts": ctx.tool_receipts}
        for stat, delta in (ctx.parsed.get("stat_changes") or {}).items():
            try:
                d = int(delta)
            except (TypeError, ValueError):
                continue
            sr = eng.validate_stat_delta(receipt_ctx, str(stat), d)
            if not sr.allowed:
                for v in sr.violations:
                    ctx.add_violation(v.rule_id, v.message, "warning")

        if ctx.violations:
            logger.info(
                "[governance] %d rule violation(s) recorded this turn",
                len(ctx.violations),
            )
        return ctx
