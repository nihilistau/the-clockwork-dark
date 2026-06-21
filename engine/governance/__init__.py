"""
Governance (PR19)
=================

The "rein them in" layer. The engine already owns truth (mechanics flow through
@skill tools), but the LLM can still *claim* things in prose/JSON it didn't earn.
Governance gives a uniform, priority-ordered interceptor pipeline around a turn:

  * ``TurnContext`` — a mutable carrier threaded through PRE and POST hooks.
  * ``GovernancePipeline`` — ordered PRE (prompt shaping) + POST (audit) chains.
  * ``@interceptor`` — register an interceptor class by phase + priority.
  * ``RulesGovernor`` — wires the long-dormant SceneRulesEngine (R001–R005) into
    every Storyteller turn, recording violations (defense in depth + telemetry).

Reuses the existing ``run_pre`` interceptor shape so LoreInject/AwarenessGate
slot in unchanged.
"""

from engine.governance.context import TurnContext
from engine.governance.pipeline import (
    GovernancePipeline,
    get_governance,
    interceptor,
    reset_governance,
)

__all__ = [
    "TurnContext",
    "GovernancePipeline",
    "get_governance",
    "interceptor",
    "reset_governance",
]
