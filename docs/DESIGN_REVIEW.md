# Design Review — DESIGN.md v0.1.0

**Reviewer:** design-doc-reviewer subagent  
**Date:** 2026-06-20  
**Round:** 1

## Verdict

Strong vision; 12 issues found. Addressed in revision round 2 (see Revision Summary at bottom).

---

### Issue 1
- **Severity:** critical
- **Section:** PR Plan — PR10 / PR12 dependencies
- **Description:** PR10 omitted PR7+PR8 dependencies required for vertical slice NPCs and caravan events.
- **Suggestion:** Add PR7 and PR8 as explicit dependencies of PR10 and PR12.
- **Status:** addressed

### Issue 2
- **Severity:** critical
- **Section:** PR Plan — PR3 / Evaluator scope
- **Description:** CODE_BRIEF required Evaluator in PR3 but Evaluator is PR5.
- **Suggestion:** PR3 tests SceneRulesEngine only; Evaluator anti-hallucination deferred to PR5.
- **Status:** addressed

### Issue 3
- **Severity:** major
- **Section:** Key Decisions / Game Mechanics
- **Description:** `story_pressure` missing from GameState; EventEngine/PlotFormula undefined.
- **Suggestion:** Add `story_pressure` to GameState; add `engine/game/plot.py`.
- **Status:** addressed

### Issue 4
- **Severity:** major
- **Section:** EvilTicker / Travel / Awareness
- **Description:** location_multiplier, awareness_delta missing from location schema; crossroads not canonical.
- **Suggestion:** Extend LOCATIONS schema; document EvilTicker units.
- **Status:** addressed

### Issue 5
- **Severity:** major
- **Section:** PR1 / PR2 scaffold
- **Description:** PR1 omitted launcher.py, config.py, dice.py ownership.
- **Suggestion:** Align PR1/PR2 file lists.
- **Status:** addressed

### Issue 6
- **Severity:** major
- **Section:** PR3 Skills
- **Description:** Skill file paths ambiguous; SceneRulesEngine rules unspecified; trade data missing.
- **Suggestion:** Canonical deliverables table; data/economy.yaml; enumerated rules.
- **Status:** addressed

### Issue 7
- **Severity:** major
- **Section:** DESIGN ↔ CODE_BRIEF consistency
- **Description:** Skill/tag manifest drift between docs.
- **Suggestion:** Shared manifest appendix in DESIGN.md.
- **Status:** addressed

### Issue 8
- **Severity:** major
- **Section:** PR11 vs PR5
- **Description:** Lore interceptor before RAG seed.
- **Suggestion:** PR5 accepts stub lore; PR11 before PR5 full integration.
- **Status:** addressed

### Issue 9
- **Severity:** minor
- **Section:** Dice / Combat / Crafting
- **Description:** Engine tables and inventory schema undefined.
- **Suggestion:** data/tables/ YAML; inventory schema; combat labeled v0.2.
- **Status:** addressed

### Issue 10
- **Severity:** minor
- **Section:** Key Decisions
- **Description:** Missing save versioning, FlaskScene ownership, JSON fallback.
- **Suggestion:** Implementation decisions table added.
- **Status:** addressed

### Issue 11
- **Severity:** minor
- **Section:** Procgen / Media
- **Description:** ProcgenResult schema missing; cutscene gate unspecified.
- **Suggestion:** ProcgenResult on GameState; CutsceneBudgetInterceptor in PR9.
- **Status:** addressed

### Issue 12
- **Severity:** nit
- **Section:** PR sizing
- **Description:** Large PRs without sizing.
- **Suggestion:** T-shirt sizes added to PR plan.
- **Status:** addressed

## Revision Summary (Round 2)

All 12 issues addressed in DESIGN.md v0.1.1. PR1–PR3 implemented with 20 passing tests.

## Re-Review (Round 2)

- **Open issues:** 0
- **PR1–PR3 alignment:** DESIGN.md PR plan matches implemented files
- **Evaluator scope:** Correctly deferred to PR5; PR3 uses SceneRulesEngine only