"""
Oracle — turn telemetry & metrics (PR30)
========================================

A slim observability backbone (CosySim Oracle, trimmed). Every turn payload is
recorded into a ring buffer and rolled into aggregates, so the system that all
the prior phases produce — eval scores, governance violations, the Assistant's
intervention/gift rate, evil drift — becomes *visible* via `/api/metrics`.

Pure in-memory and side-effect-free: feed it a turn payload; read aggregates.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TurnRecord:
    turn: int
    latency_ms: float
    eval_overall: float
    eval_passed: bool
    violations: int
    assistant_spoke: bool
    assistant_intent: str
    gift: bool
    tools: int
    evil_progress: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn": self.turn,
            "latency_ms": round(self.latency_ms, 1),
            "eval_overall": round(self.eval_overall, 3),
            "eval_passed": self.eval_passed,
            "violations": self.violations,
            "assistant_spoke": self.assistant_spoke,
            "assistant_intent": self.assistant_intent,
            "gift": self.gift,
            "tools": self.tools,
            "evil_progress": round(self.evil_progress, 4),
        }


class Oracle:
    """In-memory turn metrics with a recent-turn ring buffer."""

    def __init__(self, *, ring: int = 200) -> None:
        self._ring: deque[TurnRecord] = deque(maxlen=ring)
        self._turns = 0
        self._eval_pass = 0
        self._eval_sum = 0.0
        self._violation_turns = 0
        self._violations_total = 0
        self._assistant_spoke = 0
        self._gifts = 0
        self._latency_sum = 0.0
        self._last_evil = 0.0

    def record_turn(
        self,
        payload: dict[str, Any],
        *,
        latency_ms: float = 0.0,
        evil_progress: float = 0.0,
    ) -> TurnRecord:
        ev = payload.get("evaluation") or {}
        gov = payload.get("governance") or []
        asst = payload.get("assistant") or {}
        rec = TurnRecord(
            turn=self._turns + 1,
            latency_ms=float(latency_ms),
            eval_overall=float(ev.get("overall", 0.0)),
            eval_passed=bool(ev.get("passed", False)),
            violations=len(gov),
            assistant_spoke=bool(asst.get("spoke", False)),
            assistant_intent=str(asst.get("intent", "silent")),
            gift=bool(asst.get("gift")),
            tools=len(payload.get("tool_receipts") or []),
            evil_progress=float(evil_progress),
        )
        self._ring.append(rec)
        self._turns += 1
        self._eval_sum += rec.eval_overall
        if rec.eval_passed:
            self._eval_pass += 1
        if rec.violations:
            self._violation_turns += 1
            self._violations_total += rec.violations
        if rec.assistant_spoke:
            self._assistant_spoke += 1
        if rec.gift:
            self._gifts += 1
        self._latency_sum += rec.latency_ms
        self._last_evil = rec.evil_progress
        return rec

    def metrics(self) -> dict[str, Any]:
        n = self._turns or 1
        return {
            "turns": self._turns,
            "eval_pass_rate": round(self._eval_pass / n, 3),
            "avg_eval": round(self._eval_sum / n, 3),
            "violation_rate": round(self._violation_turns / n, 3),
            "violations_total": self._violations_total,
            "assistant_intervention_rate": round(self._assistant_spoke / n, 3),
            "gifts": self._gifts,
            "avg_latency_ms": round(self._latency_sum / n, 1),
            "last_evil_progress": round(self._last_evil, 4),
        }

    def recent(self, n: int = 20) -> list[dict[str, Any]]:
        items = list(self._ring)[-n:]
        return [r.to_dict() for r in items]


_oracle: Optional[Oracle] = None


def get_oracle() -> Oracle:
    global _oracle
    if _oracle is None:
        _oracle = Oracle()
    return _oracle


def reset_oracle() -> None:
    global _oracle
    _oracle = None
