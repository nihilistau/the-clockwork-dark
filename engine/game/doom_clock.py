"""
The Doom Clock (PR28)
=====================

The slow darkness made legible. The Clockwork Dark advances on world ticks
(``EvilTicker``, modulated by player ``engagement``); the Doom Clock layers the
*story* on top:

  * **arcs** — quiet_life → whisper → march → convergence → consumed, derived
    from evil_progress + awareness. The baker can sit in quiet_life a long time.
  * **beats** — once-only world signs the Dark crosses as it spreads (cog-harvesters
    in the wheat, the brass scarecrow waking, clockwork-vines breaching the forest,
    the tunnels opening, the tower assembling). Beats steer the Narrator and can
    fire a cutscene.
  * **consumed** — at evil_progress 1.0 the world is taken; the game ends, whether
    or not the player ever lifted a finger.

This is a *read/coordinate* layer: it reacts to the current evil_progress rather
than advancing it, so it composes cleanly with the existing ticker.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from engine.config import get_config
from engine.game.evil_ticker import phase_index
from engine.game.state import GameState

ARC_QUIET = "quiet_life"
ARC_WHISPER = "whisper"
ARC_MARCH = "march"
ARC_CONVERGENCE = "convergence"
ARC_CONSUMED = "consumed"


@dataclass(frozen=True)
class Beat:
    """A once-only world sign the Dark crosses."""

    threshold: float
    id: str
    text: str
    cutscene_id: str = ""


# Ordered by threshold — the visible spread of the Clockwork Dark.
DOOM_BEATS: tuple[Beat, ...] = (
    Beat(0.12, "harvest_south",
         "Out past the south wheatfield the stalks have begun to stand in rows too "
         "straight for any wind — and something low and brass moves between them, harvesting.",
         "cutscene_spider_wheat"),
    Beat(0.28, "scarecrow_wakes",
         "The scarecrow in the east field has turned. Its stitched grin now shows brass "
         "teeth, and its head follows the road when it thinks no one is watching.",
         "cutscene_blueprint"),
    Beat(0.46, "vines_breach_forest",
         "Cold filigree threads the birches at the forest margin — clockwork-vines, "
         "creeping inward, ticking faintly where the sap should run.",
         "cutscene_clockwork_vines"),
    Beat(0.64, "tunnels_open",
         "Beneath the old stump a seam of worked stone has yawned open. The tunnels "
         "under Edgewood are unsealed, breathing a draught that smells of oil and old time.",
         "cutscene_hidden_tunnel"),
    Beat(0.82, "tower_assembles",
         "On the horizon a tower is assembling itself out of the bruised sky, gear "
         "fitting to gear, patient and enormous. It was not there yesterday.",
         "cutscene_tower"),
    Beat(1.0, "consumed",
         "The last clock-stroke falls. Edgewood folds into mechanism — bread, hearth, "
         "and name alike — and the Clockwork Dark finishes what it always meant to.",
         "cutscene_consuming_horizon"),
)


class DoomClock:
    """Arcs, beats, and the consumed ending over the evil ticker."""

    @staticmethod
    def arc(state: GameState) -> str:
        if state.evil_progress >= 1.0:
            return ARC_CONSUMED
        phase = phase_index(state.evil_phase.value)
        reveal = float(get_config().get("awareness.reveal_threshold", 20))
        if phase >= 2 or state.awareness >= 50:
            return ARC_CONVERGENCE
        if phase >= 1 or state.awareness >= 25:
            return ARC_MARCH
        if state.awareness >= reveal:
            return ARC_WHISPER
        return ARC_QUIET

    @staticmethod
    def register_engagement(state: GameState, amount: float, reason: str = "") -> float:
        """The player pushed back against the Dark — raise engagement (caps at 100)."""
        state.engagement = max(0.0, min(100.0, state.engagement + amount))
        return state.engagement

    @staticmethod
    def pending_beats(state: GameState) -> list[Beat]:
        """Return newly-crossed beats (marks them seen). Crossing 1.0 ends the game."""
        out: list[Beat] = []
        for beat in DOOM_BEATS:
            if state.evil_progress >= beat.threshold and beat.id not in state.doom_beats_seen:
                state.doom_beats_seen.append(beat.id)
                out.append(beat)
                if beat.id == "consumed":
                    state.ended = True
                    state.flags["consumed"] = True
        return out

    @staticmethod
    def latest_beat(state: GameState) -> Optional[Beat]:
        """The most advanced beat the world has already crossed (for narration tone)."""
        seen = [b for b in DOOM_BEATS if b.id in state.doom_beats_seen]
        return seen[-1] if seen else None

    @staticmethod
    def snapshot(state: GameState) -> dict[str, Any]:
        latest = DoomClock.latest_beat(state)
        return {
            "arc": DoomClock.arc(state),
            "engagement": round(state.engagement, 1),
            "evil_progress": round(state.evil_progress, 4),
            "consumed": bool(state.flags.get("consumed")),
            "latest_beat": latest.id if latest else "",
            "beats_seen": list(state.doom_beats_seen),
        }
