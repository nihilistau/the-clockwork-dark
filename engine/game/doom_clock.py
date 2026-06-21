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

import random
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
        """Return newly-crossed beats (marks them seen). Crossing 1.0 ends the game.

        Crossing a beat also applies its declarative *world effects* (flags,
        discoveries, rumors, world_events) so the Dark's spread is tangible —
        the tunnels opening unseals the hidden path, the board gains postings,
        the village chatter turns. See ``engine/game/world_effects.py``.
        """
        from engine.game.world_effects import apply_beat_effects

        out: list[Beat] = []
        for beat in DOOM_BEATS:
            if state.evil_progress >= beat.threshold and beat.id not in state.doom_beats_seen:
                state.doom_beats_seen.append(beat.id)
                apply_beat_effects(state, beat.id)
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
        snap = {
            "arc": DoomClock.arc(state),
            "engagement": round(state.engagement, 1),
            "evil_progress": round(state.evil_progress, 4),
            "consumed": bool(state.flags.get("consumed")),
            "latest_beat": latest.id if latest else "",
            "beats_seen": list(state.doom_beats_seen),
        }
        snap["convergence"] = Convergence.snapshot(state)
        return snap


# ---------------------------------------------------------------------------
# Convergence finale (PR-more-world)
# ---------------------------------------------------------------------------
#
# The late game made into a *reckoning*, not a boss bar. Once the world has crossed
# the tower beat (the Clockwork Dark assembling on the horizon), the road has been
# counting toward one place. Convergence is the approach: a short, ordered sequence
# of reckoning beats culminating in the player's **last engine-resolved choice** at
# the tower's foot. The engine adjudicates that choice; the Storyteller narrates it.
#
# This stays a *read/coordinate* layer — it never advances evil_progress. If the
# player does nothing, the existing ``consumed`` terminal still falls at 1.0,
# untouched: the clock keeps its own appointments either way (see [[the-convergence]]).

CONVERGENCE_THRESHOLD = 0.82   # mirrors the tower beat — the finale opens here

RECKONING_STAND = "stand"        # confront the logic at the tower (engine: sympathy/engagement)
RECKONING_UNMAKE = "unmake"      # turn the Dark's own naming back on it
RECKONING_WALK_AWAY = "walk_away"  # refuse the tower; carry the quiet life to the end
RECKONING_CHOICES = (RECKONING_STAND, RECKONING_UNMAKE, RECKONING_WALK_AWAY)


@dataclass(frozen=True)
class ReckoningBeat:
    """An ordered convergence beat on the approach to the tower."""

    order: int
    id: str
    text: str
    cutscene_id: str = ""


# The approach. Reuses cutscene_tower / cutscene_consuming_horizon where it fits —
# these are not new world-signs (those are DOOM_BEATS); they are the *finale's*
# narrative spine, fired in order once the player walks the convergence in.
RECKONING_BEATS: tuple[ReckoningBeat, ...] = (
    ReckoningBeat(
        0, "horizon_counts",
        "The milestones have stopped pretending to measure distance. Each one shows "
        "a smaller number, and the tower on the horizon is no longer on the horizon.",
        "cutscene_consuming_horizon"),
    ReckoningBeat(
        1, "road_remembers_you",
        "The road has begun to say your name as you walk it — not aloud, but in the "
        "rhythm of the gears under the wheat, fitting itself to the shape of your going.",
        ""),
    ReckoningBeat(
        2, "tower_foot",
        "You stand at the tower's foot. It is not a fortress; it is a mechanism with a "
        "door, patient as a clock, and it has been waiting for exactly one more part.",
        "cutscene_tower"),
    ReckoningBeat(
        3, "the_reckoning",
        "There is a place for you inside the works. The Clockwork Dark does not hate "
        "you — it would simply make you *legible*, and finish. What you do here is the "
        "last thing the clock did not already know.",
        "cutscene_tower"),
)


@dataclass
class ReckoningResult:
    """Outcome of the player's last engine-resolved choice at the tower."""

    choice: str
    success: bool
    outcome: str
    message: str
    engagement: float = 0.0
    evil_progress: float = 0.0
    ended: bool = False
    dice: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "choice": self.choice,
            "success": self.success,
            "outcome": self.outcome,
            "message": self.message,
            "engagement": round(self.engagement, 1),
            "evil_progress": round(self.evil_progress, 4),
            "ended": self.ended,
            "dice": self.dice,
        }


class Convergence:
    """The finale layer: the approach to the tower and the last choice.

    Engine-authoritative. The reckoning choice resolves on a d20 lifted by the
    player's engagement (the line they have held) versus a DC lifted by how far the
    Dark has come — so a player who never pushed back cannot simply talk the clock
    down at the end, and an engaged one is not guaranteed either.
    """

    @staticmethod
    def is_open(state: GameState) -> bool:
        """True once the world has reached the convergence finale (tower-era)."""
        if state.evil_progress >= 1.0:
            return False  # already consumed
        return (
            state.evil_progress >= CONVERGENCE_THRESHOLD
            or DoomClock.arc(state) == ARC_CONVERGENCE
            and "tower_assembles" in state.doom_beats_seen
        )

    @staticmethod
    def pending_reckoning_beats(state: GameState) -> list[ReckoningBeat]:
        """Return newly-crossed reckoning beats in order (marks them seen).

        Only fires once the finale is open. Tracked on ``flags`` with a
        ``reckoning_`` prefix so it composes with existing state without new fields.
        """
        if not Convergence.is_open(state):
            return []
        out: list[ReckoningBeat] = []
        for beat in RECKONING_BEATS:
            key = f"reckoning_{beat.id}"
            if not state.flags.get(key):
                state.flags[key] = True
                out.append(beat)
        return out

    @staticmethod
    def reckoning_dc(state: GameState) -> int:
        """The DC for the last choice — harder the further the Dark has come."""
        cfg = get_config().get("doom", {}) or {}
        base = int(cfg.get("reckoning_base_dc", 12))
        # 0.82..1.0 maps to +0..+~9 on top of base.
        over = max(0.0, state.evil_progress - CONVERGENCE_THRESHOLD)
        span = max(1e-6, 1.0 - CONVERGENCE_THRESHOLD)
        return base + int(round((over / span) * 9))

    @staticmethod
    def resolve_reckoning(
        state: GameState,
        choice: str,
        *,
        rng: Optional[random.Random] = None,
    ) -> ReckoningResult:
        """Adjudicate the player's last engine-resolved choice at the tower.

        ``walk_away`` always succeeds (refusing the tower is always allowed — the
        quiet life carried to its end). ``stand`` and ``unmake`` roll d20 +
        engagement-bonus vs the reckoning DC; success ends the game un-consumed
        (the line held), failure leaves the clock to finish on its own.
        """
        from engine.game.dice import roll_dice

        if not Convergence.is_open(state):
            return ReckoningResult(
                choice=choice, success=False, outcome="not_open",
                message="The tower is not yet at hand.",
                engagement=state.engagement, evil_progress=state.evil_progress,
            )
        if choice not in RECKONING_CHOICES:
            return ReckoningResult(
                choice=choice, success=False, outcome="invalid",
                message=f"Unknown reckoning choice: {choice}.",
                engagement=state.engagement, evil_progress=state.evil_progress,
            )

        if choice == RECKONING_WALK_AWAY:
            # Refusal: the player turns from the tower. The world is not saved, but
            # the player is not unmade either — they carry the quiet life out.
            state.flags["reckoning_resolved"] = True
            state.flags["walked_away"] = True
            state.ended = True
            return ReckoningResult(
                choice=choice, success=True, outcome="walked_away",
                message=(
                    "You turn your back on the door. The clock does not stop — but it "
                    "finishes without you in it. You walk home the long way, and the "
                    "bread, at least, is still warm."
                ),
                engagement=state.engagement, evil_progress=state.evil_progress,
                ended=True,
            )

        dc = Convergence.reckoning_dc(state)
        bonus = int(min(8, state.engagement // 12))  # the line you held lifts the roll
        die = roll_dice(20, modifier=bonus, reason=f"reckoning:{choice}", rng=rng)
        won = die.critical or (not die.fumble and die.total >= dc)
        state.flags["reckoning_resolved"] = True

        if won:
            # The line held at the last. The Dark does not finish; it is held — never
            # banished (the Clockwork Dark is a logic, not a demon), but stopped here.
            DoomClock.register_engagement(state, 25.0, f"reckoning:{choice}")
            state.flags["reckoning_held"] = True
            state.ended = True
            msg = (
                "You name the tower's making and refuse to be a part it can use. The "
                "gears do not stop turning — but they turn without the village in their "
                "teeth. The horizon settles. It is not victory. It is enough."
                if choice == RECKONING_UNMAKE else
                "You stand in the works and hold. The mechanism reaches for the shape "
                "of you and finds it already given, already willed, already known — and "
                "for once that is a wall it cannot model past. The clock keeps its hour, "
                "but Edgewood is not in it."
            )
            return ReckoningResult(
                choice=choice, success=True, outcome="held", message=msg,
                engagement=state.engagement, evil_progress=state.evil_progress,
                ended=True, dice=die.to_dict(),
            )

        # Failure: the choice was not enough. The clock is left to finish on its own
        # — we do NOT force-consume here; the existing terminal falls at 1.0 in time.
        state.flags["reckoning_failed"] = True
        return ReckoningResult(
            choice=choice, success=False, outcome="not_enough",
            message=(
                "You reach for the words, and the words are already the clock's. The "
                "mechanism takes the shape of your trying and folds it in. The door is "
                "still open. There may be time for one more thing — or there may not."
            ),
            engagement=state.engagement, evil_progress=state.evil_progress,
            dice=die.to_dict(),
        )

    @staticmethod
    def snapshot(state: GameState) -> dict[str, Any]:
        """Finale state for narration/UI (always present; ``open`` gates it)."""
        beats_seen = [b.id for b in RECKONING_BEATS if state.flags.get(f"reckoning_{b.id}")]
        return {
            "open": Convergence.is_open(state),
            "reckoning_dc": Convergence.reckoning_dc(state) if Convergence.is_open(state) else 0,
            "reckoning_beats_seen": beats_seen,
            "resolved": bool(state.flags.get("reckoning_resolved")),
            "outcome": (
                "held" if state.flags.get("reckoning_held")
                else "walked_away" if state.flags.get("walked_away")
                else "failed" if state.flags.get("reckoning_failed")
                else ""
            ),
        }
