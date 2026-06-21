---
type: Lore
title: The Tunnel Mouth
description: The set-piece descent beneath Edgewood — a branching, engine-adjudicated discovery unlocked when the Doom Clock opens the tunnels.
tags: [lore, tunnels, set-piece, discovery, challenge, doom]
resource: data/set_pieces.yaml
timestamp: 2026-06-22
---

# The Tunnel Mouth

When the Clockwork Dark crosses the `tunnels_open` beat, the seam beneath the old
stump yawns into a ring of worked brass — and the hidden path it unseals is not
just a new location ([[beneath-the-tunnels]]) but a **set-piece**: a discovery the
player *descends into and experiences*, not a quest handed over.

## What it is

The tunnel-mouth is an authored `decision_tree` challenge
([[ephemeral-challenges]]) in `data/set_pieces.yaml`, presented by the
`start_set_piece` skill once the world has opened its ground (it is `requires_flag:
tunnels_open` / `requires_discovery: hidden_path` — you cannot descend a tunnel
that has not been unsealed; see [[the-reactive-world]]). The **engine adjudicates
every step** — the Storyteller narrates the dark, but the branches, the dead-ends,
and the outcomes are the engine's.

## The descent

A branching way down, each fork its own scene:

- **The ring** — read the worn carvings (a clue: *the low road keeps its head; the
  bright road keeps the hour; follow the water down, never the gears*) or simply
  climb in.
- **A / B** — the low crawl, or the dry clock-face tunnel where a brass-ribbed
  thing comes apart toward you.
- **D / E / F** — a flooded rail junction; only the arch the water runs down leads
  true. The wrong way is the easy way.
- **G / H** — the vaulted clockwork chamber, where a mechanism patient as a heart
  holds the seam of cold light open. This is what keeps the tunnels breathing.

## Outcomes (engine-granted)

- **Sealed** — jam the mechanism: the seam grinds shut, `tunnel_sealed` is set,
  engagement rises, and you climb out with an iron key. The objective of the
  *Seal the Tunnel* posting ([[the-notice-board]]) genuinely met.
- **Relic** — pry a brass artefact loose and leave; the seam breathes on.
- **Collapse / Lost / Retreat** — the wrong arch, the ceiling, or simple prudence:
  you come out hurt, cold, or empty-handed, and the tunnels stay open.

The carvings are the puzzle: a player who reads them, and remembers *low, and with
the water*, walks the safe path to the seam. One who doesn't, gambles. Either way
the clock keeps its hour. See [[the-convergence]].
