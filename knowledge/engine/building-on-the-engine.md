---
type: Reference
title: Building Your Own Game on the Engine
description: How OKFS plus data files turn the Clockwork engine into a customizable RPG engine — what is game-specific, what is engine-generic, and how to retarget to a new story.
tags: [engine, okfs, reuse, retargeting, data, customization]
resource: engine/okfs/bundle.py
timestamp: 2026-06-21
---

# Building Your Own Game on the Engine

The Clockwork Dark is a *configuration* of a reusable engine, not a monolith.
The split that makes this work: code is generic; **content is data + knowledge**.
To make a new game you replace the content, not the engine.

## Game-specific (you replace this)

- **The OKFS bundle** (`knowledge/`) — lore, NPC, Item, Location, Phase and arc
  concepts. The `KnowledgeCascade` blends only the game types
  (`Lore/NPC/Item/Location/Bestiary/Phase/Faction`) into prompts; dev/reference
  docs are deliberately excluded.
- **`data/*.yaml`** — `economy.yaml`, `bestiary.yaml`, `recipes/*.yaml`,
  `contracts.yaml`, `world/content.yaml`, the `procgen_templates/`, the ComfyUI
  prompts (`comfyui.yaml`), voice config, and the asset `manifest.yaml`.
- **Canon IDs** — agent ids, location ids, evil-phase names, the system prompts
  and tone lines.

## Engine-generic (you keep this, unchanged)

Dice, skill checks, combat, crafting, the evil ticker and Doom Clock, ephemeral
challenges, contracts, the `@skill` registry, the two agents, the governance
pipeline + `SceneRulesEngine`, the OKFS loader/validator/cascade, and the media
and Oracle layers. None of these encode Edgewood; they read it from data and
knowledge. The engine resolves mechanics — see [[clockwork-engine]].

## Retargeting to a new story

1. **Swap the knowledge bundle** — write new OKFS concepts ([[okfs-spec]],
   conventions in [[okfs-conventions]]); the validator enforces frontmatter and
   `[[link]]` integrity, and `OKFSBundle` indexes them by slug/type/tag.
2. **Swap `data/*.yaml`** — new economy, bestiary, recipes, contracts, world
   content, and procgen templates.
3. **Rename canon IDs** — your agents, locations, phases, and tone in the system
   prompts and config.
4. **Swap the media prompts** — ComfyUI/voice templates and the asset manifest.

The engine is untouched: the same turn loop, the same skill-gated truth, the same
governance. You have changed *what* the world is, not *how* it runs. To add new
mechanics rather than reskin existing ones, see [[extending-the-engine]].
