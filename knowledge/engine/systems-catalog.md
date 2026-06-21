---
type: Reference
title: Systems Catalog
description: Every gameplay system at a glance, with its key @skill tool names and the data files that feed it.
tags: [reference, systems, skills, tools, mechanics, data]
resource: engine/skills/builtin/mechanics.py
timestamp: 2026-06-21
---

# Systems Catalog

Every player-facing system resolves through engine-authoritative `@skill` tools
(registered in `engine/skills/registry.py`, dispatched by
`engine/agents/tool_dispatcher.py`). The LLM narrates; the engine decides. This
is the index — follow the links for depth.

**Dice & skill checks** — `roll_dice(sides, modifier, reason)` and
`resolve_skill_check(skill, dc, modifier)`. Both `TRIGGER_REQUIRED`: the
Storyteller must call them before narrating any roll. Logic in `engine/game/dice.py`.

**Grounded combat** — `resolve_combat(action, target_id, item_id)` with `action`
in {attack, defend, flee, use_item, sympathy}; snapshot via `query_combat_state`.
Foes load from `data/bestiary.yaml`; resolution in `engine/game/combat.py`.

**Crafting** — `craft_item(recipe_id)` and `list_recipes`. The engine checks
station, verifies inputs, rolls `d20 + stat//5 vs dc`, then consumes and grants.
Recipes in `data/recipes/*.yaml` (`engine/game/crafting.py`).

**Travel** — `move_to(location_id)` walks the `scene_graph` in
`data/world/content.yaml` (exits carry hours, danger_dc, awareness_delta).

**Trade** — `trade(action, item_id, npc_id)` with browse/buy/sell against vendor
prices in `data/economy.yaml`.

**The Doom Clock** — `confront_darkness(intensity)` raises *engagement*, holding
back the slow darkness. *Arcs* (quiet_life→consumed) and once-only *beats* live
in `engine/game/doom_clock.py`. See [[doom-arcs]].

**The reactive world** — crossing a beat *changes the world*: flags, discoveries
(the tunnels opening unseals the hidden path), rumors, and notice-board postings,
all from `data/world/doom_effects.yaml` (`engine/game/world_effects.py`). The
Dark's spread is something you walk into. See [[the-reactive-world]].

**Ephemeral challenges** — `start_challenge(spec)` / `resolve_challenge(choice,
answer)`. Kinds: skill_gauntlet, decision_tree, puzzle, dice_table
(`engine/game/challenges.py`). The AI supplies structure; the engine adjudicates.
See [[ephemeral-challenges]].

**Contracts** — `list_contracts` / `accept_contract` / `complete_contract`,
backed by `data/contracts.yaml`. Opt-in work; rewards are engine-granted. See
[[the-notice-board]].

**The Assistant** — `grant_hint`, `reveal_lore`, `change_form`, `assistant_gift`
(`engine/skills/builtin/assistant.py`), trust- and awareness-gated.

**Knowledge** — `query_knowledge(query)` / `read_concept(slug)` read this OKFS
bundle at runtime.

**Media tags** — narration may embed `[IMAGE:...]`, `[CUTSCENE:...]`,
`[VOICE:...]` for ComfyUI / cutscene / TTS.

**The Oracle** — per-turn telemetry served at `/api/metrics`
(`engine/observability/oracle.py`). See [[turn-metrics]].

Architecture overview: [[clockwork-engine]]. To add a system, see
[[extending-the-engine]].
