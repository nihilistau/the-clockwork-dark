# Review & Audit — The Clockwork Dark

_Date: 2026-06-21 · Scope: full codebase + design-asset integration · Baseline: PR1–PR11 complete._

## Summary

The project is in good health. The deterministic engine, dual-agent layer, media
pipeline, RAG lore, and Flask/Socket.IO scene are all implemented and tested. The
design system was bundled but not fully *driving* the UI; that gap is now closed
(see Phase C). No golden-rule violations remain after one fix.

| Area | Status |
|------|--------|
| Test suite | ✅ 123 passing (`pytest tests/ -q`, ~43s) |
| Config discipline (no hardcoded ports/models/paths) | ✅ after fix (see below) |
| Engine-resolves-mechanics boundary | ✅ enforced via `@skill` registry + Evaluator |
| Canon IDs (agents, locations, phases) | ✅ unchanged |
| Design-asset integration | ✅ now default + local-first |

## Tests

`pytest tests/ -q` → **123 passed**. 21 suites cover dice, evil ticker, locations,
skills enforcement, stream processing, storyteller/assistant agents, evaluator,
media, procgen, world-sim, lore/awareness, saves, the Flask scene, the design
manifest, and the PR12 vertical slice. The vertical-slice smoke test exercises all
nine PR12 acceptance criteria end-to-end with a mock LLM.

## Config discipline

All external endpoints and model names are resolved **config-first** with sensible
fallback defaults, e.g. `cfg.get("lmstudio.base_url", "http://localhost:1234/v1")`
(`engine/lmstudio/client.py`, `engine/media/{comfyui,tts,stt}.py`,
`engine/lmstudio/profiles.py`). These are correct, not violations.

**Fixed:** `engine/design/assets.py` previously hardcoded
`C:\Projects\clockwork-dark\Design_files` as a resolution fallback. Replaced with
repo-relative resolution (env `CLOCKWORK_DESIGN_FILES` → config `paths.design_files`
→ bundled `<repo>/Design_files`). `config/default.yaml` now defaults
`paths.design_files` to the repo-relative `"Design_files"` instead of a bare
`${CLOCKWORK_DESIGN_FILES}` env reference, so a fresh clone renders the full design
system with zero setup.

## Engine ↔ LLM boundary

The hard engine owns all mechanics; LLMs only narrate. Stat/inventory/travel/dice
changes flow exclusively through the `@skill` registry (`engine/skills/`), and the
Evaluator (`engine/agents/evaluator.py`) gates hallucinated mechanics with a retry.
`test_skill_enforcement.py` and `test_storyteller.py` cover this.

## Design-asset integration (resolved)

- **Media** (scene stills, intro, cutscenes, dice videos, portraits, items) was
  already mapped through `data/assets/manifest.yaml` + the `/design/<path>` Flask
  route. Verified: **113/113 referenced asset URLs exist on disk** (0 dangling).
- **Styling gap closed:** design tokens, the four type voices, and the phase-theme
  CSS now drive the live UI by default (previously behind a fragile conditional).
- **Local-first:** fonts were loading from the Google Fonts CDN; the four families
  are now vendored as `.woff2` under `Design_files/assets/fonts/` and served by the
  app, so play works fully offline.
- **Verified in-browser** (Playwright): `/design/styles.css` linked, fonts load
  locally, start screen + menu art + wordmark + 3 archetypes render, and the
  phase-theme creep advances `--surface-scene` (`#080b0b`→`#050706`) and
  `--corruption-reveal` (`0`→`1`) across dormant→consuming.

## Repository hygiene

Private repo `nihilistau/the-clockwork-dark`. `.gitignore` excludes the 8 redundant
ZIP source-bundles (incl. a 97 MB archive) and the `art-min/` duplicate; all runtime
art/video/tokens are committed (~340 MB) so a clone runs. `.gitattributes` normalizes
line endings and marks binaries. No committed file approaches GitHub's 100 MB limit.

## Operational note

Two leftover Flask servers from prior sessions were holding port 5573 and serving a
pre-start-screen template — a stale-process gotcha, not a code defect. `scripts/start.ps1`
should free the port before launch; consider adding a port-kill guard.

## Recommendations / next

1. **v0.2 features** (in progress): grounded combat (`resolve_combat`), crafting
   (`craft_item`), Millhaven march arc + cutscene milestones — each engine-authoritative
   and test-driven.
2. Optional: self-host the Socket.IO client (currently a CDN `<script>`) for full
   offline parity.
3. Optional: add a `start.ps1` port-free guard to avoid the stale-process gotcha.
