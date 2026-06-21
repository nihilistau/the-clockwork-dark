---
type: Reference
title: Ephemeral Structured Challenges
description: AI-composed, engine-resolved encounters — dice gauntlets, decision trees, and puzzles with rigid schemas.
tags: [challenges, mechanics, tools, engine, ai]
resource: engine/game/challenges.py
timestamp: 2026-06-21
---

# Ephemeral Structured Challenges

The Storyteller can *compose* a rule-bound encounter mid-narration but cannot
cheat its outcome. The AI supplies a declarative **spec** (validated against a
fixed schema); `engine/game/challenges.py` owns resolution — rolling dice,
walking the tree, checking the answer. This is the property no scripted game has:
an improvising narrator that hands the *deterministic engine* a fresh, rigid
mechanic to adjudicate.

## Kinds
- **skill_gauntlet** — an ordered sequence of `d20 + stat//5 vs dc` checks; pass
  all → reward, any fail → fail effect.
- **decision_tree** — branching `nodes` with `options` and terminal outcomes.
- **puzzle** — a normalized typed answer vs the solution, with N attempts.
- **dice_table** — a weighted random outcome table.

## Tools
- `start_challenge(spec)` — validate + present the first step (sets `state.challenge`).
- `resolve_challenge(choice|answer)` — advance one step; `skill_gauntlet`/`dice_table`
  just attempt/roll. Effects (engagement / item / hp / stamina / awareness) apply
  engine-authoritatively; the challenge persists across turns and save/load.

The notice board, a tinker's bargain, the seam under the stump — any of these can
be a challenge. It pairs naturally with [[doom-arcs]] engagement and the
governance/[[clockwork-architecture]] "engine resolves, LLM proposes" rule.

Related: [[clockwork-architecture]]
