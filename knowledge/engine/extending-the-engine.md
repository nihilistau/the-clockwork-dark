---
type: Runbook
title: Extending the Engine
description: How to add a @skill tool, a governance interceptor, a challenge kind, or an OKFS concept — the engine-authoritative way.
tags: [runbook, extending, skills, governance, challenges, okfs, developer]
resource: engine/skills/registry.py
timestamp: 2026-06-21
---

# Extending the Engine

Four common extension points. The golden rule throughout: **the engine resolves;
the LLM narrates.** Never let a tool trust the model for an outcome.

## Add a @skill tool

Write a function returning a JSON string and decorate it with
`@skill(pack=..., description=..., category=..., trigger=...)` from
`engine/skills/registry.py`. Get the engine via `get_active_engine()` and mutate
state only through engine methods — the tool owns the outcome (see
`roll_dice`/`craft_item` in `engine/skills/builtin/mechanics.py`). Put it in an
`engine/skills/builtin/*.py` module, then **register it by importing that module**
in `engine/agents/tool_dispatcher.py` (the `# noqa: F401` imports trigger the
decorator). Use `trigger=TRIGGER_REQUIRED` for anything the Storyteller must call
before narrating (dice, combat, travel).

## Add a PRE/POST interceptor

Decorate a class with `@interceptor("pre"|"post", priority=N)` from
`engine/governance/pipeline.py`. PRE classes implement
`run_pre(state, system_prompt, *, player_action)` and return a shaped prompt;
POST classes implement `run_post(ctx)` and mutate the `TurnContext` (record
violations, queue media). Define it in `engine/governance/governors.py`, then
enable it by name in `config/default.yaml` under `comms.interceptors` (PRE) or
`governance.post` (POST). Interceptors run priority-ordered and must never break
a turn.

## Add an ephemeral challenge kind / spec

To author a *new spec* of an existing kind, just pass a `start_challenge(spec)`
object with `kind` in {skill_gauntlet, decision_tree, puzzle, dice_table}. To add
a *new kind*, extend `KINDS`, the `start_challenge` validator, and a `_resolve_*`
resolver in `engine/game/challenges.py`, applying outcomes through
`_apply_effects` (engagement / item / hp / stamina / awareness / `set_flags`). See
[[ephemeral-challenges]].

For a **discoverable, authored** challenge — a *set-piece* like the tunnel-mouth
descent — add the spec to `data/set_pieces.yaml` with an optional
`requires_flag` / `requires_discovery` gate, and present it with the
`start_set_piece(id)` skill once the world has reached it (`engine/game/set_pieces.py`).
Node `image` / `riddle` fields render as scene art + a parchment clue in the
challenge overlay. See [[the-tunnel-mouth]] and [[the-reactive-world]].

## Add an OKFS concept

Create one Markdown file with required frontmatter (type, title, description;
plus tags, resource, timestamp) under `knowledge/`. Link siblings with `[[slug]]`
— only to slugs that exist. Run `python scripts/build_okfs_index.py` to refresh
`knowledge/_index.json`, then keep tests green (`pytest` — the index and
link-validation tests fail on drift or broken links). Format details in
[[okfs-spec]].

Catalogue of what's already here: [[systems-catalog]]. System shape:
[[clockwork-engine]]. Retargeting to a new game: [[building-on-the-engine]].
