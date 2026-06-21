---
type: Lore
title: The Doom Clock — Arcs & Engagement
description: How the slow darkness paces — quiet_life to consumed — and how the player holds it back.
tags: [lore, doom, pacing, arcs, engagement, mechanics]
resource: engine/game/doom_clock.py
timestamp: 2026-06-21
---

# The Doom Clock — Arcs & Engagement

The Clockwork Dark advances on world ticks. The Doom Clock (`engine/game/doom_clock.py`)
turns that drift into a story the player *experiences*, not one thrust on them.

## Arcs
Derived from evil_progress + awareness:
- **quiet_life** — the baker's arc. You may live here a long time, blissfully
  unaware, the dark only a rumor at the edge of hearing.
- **whisper** — you have begun to notice. Rumors, anomalies, the Assistant's
  warnings start to land.
- **march** — the road inward opens (the Marches, Millhaven); the dark is
  undeniable to the watchful.
- **convergence** — the late game; names are hunted, the horizon comes apart.
- **consumed** — the terminal ending. If the player never pushes back, the world
  is taken anyway. The clock does not wait for a hero.

## Engagement — holding the dark back
`engagement` (0–100) rises when the player confronts the Dark: defeating
clockwork foes, clearing vines, sealing a seam, the `confront_darkness` skill.
High engagement slows the tick (up to ~40%); it decays, so the player must keep
pushing. This is the lever: a quiet baker lets the clock run fast; an engaged
wanderer can hold the line — but never stop it alone.

The **Oracle** ([[turn-metrics]]) watches the pacing so the timing — the heart of
the dread — stays right. See [[the-harvest]] for the signs and [[the-two-powers]]
for who is turning the clock.
