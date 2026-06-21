---
type: Log
title: Changelog — The Clockwork Engine
description: A running, append-only log of meaningful changes — OKFS used on ourselves.
tags: [log, changelog, okfs, history]
resource: knowledge/_index.json
timestamp: 2026-06-21
---

# Changelog — The Clockwork Engine

We keep this as a live example: OKFS used *on ourselves*. Append newest at top.
Each entry is a date, a one-line summary, and the OKFS `bundle_hash` after the
change (see [[okfs-spec]] and `knowledge/_index.json`).

## 2026-06-21
- **OKFS hashing + index** — every concept now carries a content hash; the bundle
  a roll-up hash. `scripts/build_okfs_index.py` writes the lockfile
  `knowledge/_index.json`; a test fails if it goes stale. This changelog added.
- **The soul shipped** — Doom Clock ([[doom-arcs]], [[the-harvest]]), the unreliable
  Assistant Director, ephemeral [[ephemeral-challenges]] challenges, and the
  [[the-notice-board]] contracts. The two powers: [[the-two-powers]].
- **Foundations** — live LLM loop hardened (streaming, [[lmstudio-structured-output]],
  resilience), governance pipeline wiring SceneRulesEngine, OKFS knowledge backbone,
  ComfyUI/Voxtral setup ([[install-comfyui]], [[install-voxtral]], [[run-on-the-beast]]).
- **Observability** — the Oracle ([[turn-metrics]]) for pacing.

See [[clockwork-architecture]] for the system and [[okfs-conventions]] for why
everything — including this log — is OKFS.
