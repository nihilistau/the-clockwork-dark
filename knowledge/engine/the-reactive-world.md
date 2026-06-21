---
type: Reference
title: The Reactive World
description: How Doom Clock beats mutate the world — flags, discoveries, rumors, and notice-board postings that make the Dark's spread tangible.
tags: [world, doom, beats, discoveries, contracts, reactive, mechanics]
resource: engine/game/world_effects.py
timestamp: 2026-06-22
---

# The Reactive World

The Doom Clock's **beats** ([[doom-arcs]]) are the once-only world-signs the
Clockwork Dark crosses as it spreads — the south field falling to the harvest,
the brass scarecrow waking, clockwork-vines breaching the forest, the tunnels
opening, the tower assembling. They used to fire only narration and a cutscene.
Now each beat also **changes the world**, so the spread is something the player
walks into rather than only reads about.

## What a beat does

When `DoomClock.pending_beats` crosses a beat, `engine/game/world_effects.py`
applies that beat's declarative entry from `data/world/doom_effects.yaml`:

- **flags** — durable world state the Storyteller and interceptors can read
  (`scarecrow_awake`, `vines_breached`, `tunnels_open`, `tower_visible`).
- **discoveries** — set `discovery_<key>`, which opens edges/locations gated by
  `requires_discovery` in the scene graph. The tunnels opening literally unseals
  the road to **Hollow Hill** and the **Mage-Ruins** ([[beneath-the-tunnels]]) —
  new ground you can only reach *because the Dark opened it*.
- **rumors** — village chatter accrues, so the square and notice board reflect
  the turning world.
- **world_events** — a running ledger of what the Dark has done, kept coherent
  for narration.

Everything lands on existing `GameState` fields, so it serializes and
round-trips with the save for free; applying a beat is idempotent.

## The board responds

Notice-board postings ([[the-notice-board]]) can carry a `requires_flag` gate, so
a contract stays hidden until its world-sign falls — the village does not post a
watch for a tunnel that has not yet opened. When `tunnels_open` fires, *Seal the
Tunnel* appears; when the vines breach, *Tend the Forest Margin*; when the
scarecrow wakes, *Watch: The Walking Scarecrow*. Opt-in work that the spreading
Dark itself creates.

## Why it matters

This is the design promise made mechanical: a darkness slowly overcoming the
land, a puzzle you *experience*. The clock keeps its own appointments either way
— but as it ticks, the map widens where the Dark broke it open, the gossip turns,
and new bounties pin themselves to the board. Engine-authoritative throughout;
the Storyteller narrates what the world has already become. See
[[systems-catalog]] and [[the-harvest]].
