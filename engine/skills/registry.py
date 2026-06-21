"""
Skill Registry
==============

@skill decorator — LLM-callable mechanical tools.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

TRIGGER_AUTO = "auto"
TRIGGER_OPTIONAL = "optional"
TRIGGER_REQUIRED = "required"


@dataclass
class SkillDef:
    """Registered skill metadata."""

    name: str
    pack: str
    description: str
    category: str
    func: Callable[..., str]
    trigger: str = TRIGGER_OPTIONAL
    cooldown: float = 0.0
    cost: float = 1.0
    tags: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)


class SkillRegistry:
    """Global skill registry."""

    def __init__(self) -> None:
        self._skills: dict[str, SkillDef] = {}

    def register(self, skill_def: SkillDef) -> None:
        self._skills[skill_def.name] = skill_def

    def get(self, name: str) -> Optional[SkillDef]:
        return self._skills.get(name)

    def all_tools(self) -> list[SkillDef]:
        return list(self._skills.values())

    def get_pack_tools(self, pack: str) -> list[SkillDef]:
        return [s for s in self._skills.values() if s.pack == pack]

    def count(self) -> int:
        return len(self._skills)

    def invoke(self, name: str, **kwargs: Any) -> str:
        """Invoke skill by name; returns JSON string."""
        skill_def = self._skills.get(name)
        if skill_def is None:
            return json.dumps({"error": f"Unknown skill: {name}"})
        try:
            result = skill_def.func(**kwargs)
            return result if isinstance(result, str) else json.dumps(result)
        except Exception as exc:
            return json.dumps({"error": str(exc)})


SKILL_REGISTRY = SkillRegistry()


def skill(
    pack: str,
    description: str,
    category: str = "GAME",
    name: Optional[str] = None,
    trigger: str = TRIGGER_OPTIONAL,
    cooldown: float = 0.0,
    cost: float = 1.0,
    tags: Optional[list[str]] = None,
    prerequisites: Optional[list[str]] = None,
) -> Callable[[Callable[..., str]], Callable[..., str]]:
    """Register a skill function."""

    def decorator(func: Callable[..., str]) -> Callable[..., str]:
        skill_name = name or func.__name__
        SKILL_REGISTRY.register(
            SkillDef(
                name=skill_name,
                pack=pack,
                description=description,
                category=category,
                func=func,
                trigger=trigger,
                cooldown=cooldown,
                cost=cost,
                tags=tags or [],
                prerequisites=prerequisites or [],
            )
        )
        return func

    return decorator