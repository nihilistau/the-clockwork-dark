---
type: Lore
title: The Convergence
description: The finale — the approach to the clockwork tower and the player's last engine-resolved choice, where the road finally stops counting.
tags: [lore, finale, convergence, tower, reckoning, doom, mechanics]
resource: engine/game/doom_clock.py
timestamp: 2026-06-21
---

# The Convergence

The convergence is the late game made into a *reckoning* rather than a boss bar.
It is the last [[doom-arcs]] arc before `consumed`, and the Doom Clock
(`engine/game/doom_clock.py`) gives it real machinery: a `Convergence` layer that
opens once the world has crossed the **tower** sign ([[the-harvest]]) and then runs
the approach as an ordered sequence of reckoning beats culminating in one choice.

## The approach
Once convergence is open, the road stops pretending. The milestones count down to a
number that is not a distance; the road begins to say your name in the rhythm of the
gears under the wheat ([[sympathy-and-naming]]); and the tower — assembling on the
horizon since SPREADING — is suddenly at your foot. It is not a fortress. It is a
mechanism with a door, patient as a clock, waiting for exactly one more part.

## The last choice
At the tower's foot the engine offers the player's **last engine-resolved choice**.
The engine adjudicates; the Storyteller narrates. There are three:

- **stand** — hold in the works and refuse to be a shape the mechanism can use.
- **unmake** — turn the Dark's own naming back on it ([[sympathy-and-naming]]).
- **walk_away** — refuse the tower entirely and carry the quiet life to its end.

`walk_away` always succeeds — refusal is always allowed, and the player is not
unmade, only the world unsaved. `stand` and `unmake` roll d20 lifted by the
**engagement** the player has held (the line they kept; [[doom-arcs]]) against a DC
lifted by how far the Dark has come — so a baker who never pushed back cannot simply
talk the clock down at the end, and an engaged wanderer is not guaranteed either.

## What victory is, and is not
A held reckoning does **not** banish the Dark. The Clockwork Dark is a *logic*, not
a demon; it cannot be slain, only stopped *here*. The gears keep turning — but they
turn without the village in their teeth. The horizon settles. It is not victory.
It is enough. And if the player does nothing, or fails, the existing terminal still
falls in its own time: [[the-clockwork-dark]] keeps its own appointments either way.
