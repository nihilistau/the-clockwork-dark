"""
Governance Pipeline (PR19)
==========================

A priority-ordered registry of PRE (prompt-shaping) and POST (audit)
interceptors. PRE interceptors keep the existing
``run_pre(state, system_prompt, *, player_action) -> str`` shape so the lore and
awareness interceptors slot in unchanged; POST interceptors take a
:class:`TurnContext` and mutate it (record violations, queue media, etc.).
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Optional

from engine.config import get_config
from engine.game.state import GameState
from engine.governance.context import TurnContext

logger = logging.getLogger(__name__)

# Registries populated by the @interceptor decorator.
_PRE_REGISTRY: dict[str, type] = {}
_POST_REGISTRY: dict[str, type] = {}
_GOVERNANCE: Optional["GovernancePipeline"] = None


def interceptor(
    phase: str,
    *,
    priority: int = 50,
    name: Optional[str] = None,
) -> Callable[[type], type]:
    """Register an interceptor class by ``phase`` ("pre"/"post") + ``priority``."""

    def deco(cls: type) -> type:
        cls.priority = priority  # type: ignore[attr-defined]
        cls.name = name or cls.__name__  # type: ignore[attr-defined]
        (_PRE_REGISTRY if phase == "pre" else _POST_REGISTRY)[cls.name] = cls  # type: ignore[attr-defined]
        return cls

    return deco


class GovernancePipeline:
    """Runs ordered PRE and POST interceptors around an agent turn."""

    def __init__(
        self,
        pre: Optional[list[Any]] = None,
        post: Optional[list[Any]] = None,
    ) -> None:
        self.pre = sorted(pre or [], key=lambda i: getattr(i, "priority", 50))
        self.post = sorted(post or [], key=lambda i: getattr(i, "priority", 50))

    # --- construction ----------------------------------------------------
    @classmethod
    def from_config(cls) -> "GovernancePipeline":
        """Build from config: ``comms.interceptors`` (PRE) + ``governance.post`` (POST)."""
        cfg = get_config()
        pre_names = cfg.get("comms.interceptors", []) or []
        post_names = cfg.get("governance.post", []) or []
        pre = [_PRE_REGISTRY[n]() for n in pre_names if n in _PRE_REGISTRY]
        post = [_POST_REGISTRY[n]() for n in post_names if n in _POST_REGISTRY]
        if not post:  # sensible default even if config omits it
            post = [_POST_REGISTRY[n]() for n in ("RulesGovernor",) if n in _POST_REGISTRY]
        return cls(pre=pre, post=post)

    # --- execution -------------------------------------------------------
    def run_pre(
        self,
        state: GameState,
        system_prompt: str,
        *,
        player_action: str = "",
    ) -> str:
        result = system_prompt
        for ic in self.pre:
            fn = getattr(ic, "run_pre", None)
            if callable(fn):
                try:
                    result = fn(state, result, player_action=player_action)
                except Exception as exc:  # an interceptor must never break a turn
                    logger.warning(
                        "[governance] PRE %s failed: %s", getattr(ic, "name", ic), exc
                    )
        return result

    def run_post(self, ctx: TurnContext) -> TurnContext:
        for ic in self.post:
            if ctx.abort:
                break
            fn = getattr(ic, "run_post", None)
            if callable(fn):
                try:
                    fn(ctx)
                except Exception as exc:
                    logger.warning(
                        "[governance] POST %s failed: %s", getattr(ic, "name", ic), exc
                    )
        return ctx


def get_governance() -> "GovernancePipeline":
    """Process-wide governance pipeline (rebuilt via reset_governance)."""
    global _GOVERNANCE
    if _GOVERNANCE is None:
        # Import registers the builtin interceptors via @interceptor.
        import engine.governance.governors  # noqa: F401

        _GOVERNANCE = GovernancePipeline.from_config()
    return _GOVERNANCE


def reset_governance() -> None:
    """Clear the cached pipeline (tests / config changes)."""
    global _GOVERNANCE
    _GOVERNANCE = None
