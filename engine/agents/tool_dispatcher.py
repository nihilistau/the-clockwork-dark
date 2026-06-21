"""
Tool Dispatcher
===============

Executes @skill tools from Storyteller tool_calls and builds receipts.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import json
import logging
from typing import Any

import engine.skills.builtin.assistant  # noqa: F401 — register skills
import engine.skills.builtin.mechanics  # noqa: F401 — register skills
from engine.game.engine import GameEngine, set_active_engine
from engine.skills.registry import SKILL_REGISTRY

logger = logging.getLogger(__name__)


def execute_tool(name: str, args: dict[str, Any], engine: GameEngine) -> dict[str, Any]:
    """
    Invoke a registered skill and return receipt + raw result.

    Args:
        name: Skill name.
        args: Skill arguments.
        engine: Active game engine.

    Returns:
        Receipt dict with skill, args, result, success.
    """
    set_active_engine(engine)
    raw = SKILL_REGISTRY.invoke(name, **args)
    try:
        result = json.loads(raw)
        success = "error" not in result
    except json.JSONDecodeError:
        result = {"raw": raw}
        success = False

    receipt: dict[str, Any] = {
        "skill": name,
        "args": args,
        "result": result,
        "success": success,
    }
    if name in ("roll_dice", "resolve_skill_check"):
        receipt["type"] = "dice"
    elif name == "move_to":
        receipt["type"] = "move"
    elif name == "query_evil_state":
        receipt["type"] = "gm"
    return receipt


def execute_tool_calls(
    tool_calls: list[dict[str, Any]],
    engine: GameEngine,
) -> list[dict[str, Any]]:
    """Execute a list of tool call dicts with name/args keys."""
    receipts: list[dict[str, Any]] = []
    for call in tool_calls:
        name = call.get("name") or call.get("skill", "")
        args = call.get("args") or call.get("arguments") or {}
        if not name:
            continue
        if SKILL_REGISTRY.get(name) is None:
            logger.warning(
                "[tool_dispatcher] Unknown skill (operation=execute_tool, skill=%s)",
                name,
            )
            receipts.append(
                {
                    "skill": name,
                    "args": args,
                    "result": {"error": f"Unknown skill: {name}"},
                    "success": False,
                }
            )
            continue
        receipts.append(execute_tool(name, args, engine))
    return receipts


def auto_resolve_skill_check(
    parsed: dict[str, Any],
    engine: GameEngine,
) -> list[dict[str, Any]]:
    """
    If JSON epilogue requests skill_check, auto-call resolve_skill_check.

    Returns:
        Tool receipts (empty if no skill_check).
    """
    sc = parsed.get("skill_check")
    if not sc or not isinstance(sc, dict):
        return []
    skill = sc.get("skill", "survival")
    dc_mod = int(sc.get("dc_mod", 0))
    base_dc = 12
    dc = base_dc + dc_mod
    modifier = 0
    if skill == "stealth":
        modifier = 2
    elif skill == "persuasion":
        modifier = 1
    receipt = execute_tool(
        "resolve_skill_check",
        {"skill": skill, "dc": dc, "modifier": modifier},
        engine,
    )
    parsed["skill_check_result"] = receipt.get("result")
    return [receipt]