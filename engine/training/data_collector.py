"""
DataCollector — turn capture for self-improvement.
==================================================

Appends one JSON line per turn to ``paths.training_data`` (default
``data/training/turns.jsonl``) so the system can later be fine-tuned on its own
play. It is a *sink*, not an authority: it reads a finished turn payload and
never mutates state, never touches the hard engine, and is wrapped so it can
never break a turn (see the gated hook in ``clockwork_state.run_turn``).

Design mirrors the Oracle ([[turn-metrics]]): a slim recorder with a singleton
``get_collector()`` / ``reset_collector()`` pair. Disabled by default
(``training.collect: false``) so CI and normal play write nothing.

Captured per turn (flat, JSONL-friendly):

    session_id, turn_number, player_action, narration, choices (count),
    tool_receipts [{skill, success}], evaluation {overall, passed},
    governance (violation count), assistant {spoke, intent, gift},
    doom (snapshot if present), evil_progress, latency_ms, ts
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Optional

from engine.config import get_config

logger = logging.getLogger(__name__)

# Repo root — used to resolve repo-relative config paths (never hardcode).
_ROOT = Path(__file__).resolve().parents[2]

_DEFAULT_TRAINING_PATH = "data/training/turns.jsonl"


def _receipt_summary(receipts: Any) -> list[dict[str, Any]]:
    """Reduce tool receipts to {skill, success} pairs for compact capture."""
    out: list[dict[str, Any]] = []
    for r in receipts or []:
        if not isinstance(r, dict):
            continue
        skill = r.get("skill") or r.get("tool") or r.get("type") or ""
        result = r.get("result")
        success = r.get("success")
        if success is None and isinstance(result, dict):
            success = result.get("success")
        out.append({"skill": str(skill), "success": bool(success) if success is not None else None})
    return out


class DataCollector:
    """Appends turn records to a JSONL file (config-gated, fail-safe)."""

    def __init__(self, *, path: Optional[str] = None, enabled: Optional[bool] = None) -> None:
        # ``path=None`` means "read from config on each write" so tests can
        # monkeypatch ``paths.training_data`` freely; an explicit path pins it.
        self._path_str = path
        self._enabled_override = enabled
        self._count = 0

    @staticmethod
    def _config_path() -> str:
        cfg = get_config()
        # Honour ``paths.training_data`` (canonical key the spec names); fall
        # back to a key inside the ``training:`` block, then the default.
        return (
            cfg.get("paths.training_data")
            or cfg.get("training.data_path")
            or _DEFAULT_TRAINING_PATH
        )

    # --- config-driven knobs --------------------------------------------
    @property
    def enabled(self) -> bool:
        if self._enabled_override is not None:
            return self._enabled_override
        return bool(get_config().get("training.collect", False))

    def _resolve_path(self) -> Path:
        # Re-read each write so tests can monkeypatch the config path freely.
        path_str = self._path_str if self._path_str is not None else self._config_path()
        p = Path(path_str)
        if not p.is_absolute():
            p = _ROOT / p
        return p

    # --- capture ---------------------------------------------------------
    @staticmethod
    def build_record(
        payload: dict[str, Any],
        *,
        player_action: str = "",
        latency_ms: float = 0.0,
        evil_progress: float = 0.0,
        ts: Optional[float] = None,
        turn_number: int = 0,
    ) -> dict[str, Any]:
        """Flatten a turn payload into a JSONL-friendly training record."""
        ev = payload.get("evaluation") or {}
        gov = payload.get("governance") or []
        asst = payload.get("assistant") or {}
        choices = payload.get("choices") or []
        return {
            "session_id": payload.get("session_id", ""),
            "turn_number": turn_number,
            "player_action": player_action,
            "narration": payload.get("narration", ""),
            "choices": len(choices),
            "tool_receipts": _receipt_summary(payload.get("tool_receipts")),
            "evaluation": {
                "overall": float(ev.get("overall", 0.0)),
                "passed": bool(ev.get("passed", False)),
            },
            "governance": len(gov),
            "assistant": {
                "spoke": bool(asst.get("spoke", False)),
                "intent": str(asst.get("intent", "silent")),
                "gift": bool(asst.get("gift")),
            },
            "doom": payload.get("doom"),
            "evil_progress": float(evil_progress),
            "latency_ms": round(float(latency_ms), 1),
            "ts": float(ts) if ts is not None else time.time(),
        }

    def record(
        self,
        payload: dict[str, Any],
        *,
        player_action: str = "",
        latency_ms: float = 0.0,
        evil_progress: float = 0.0,
        ts: Optional[float] = None,
    ) -> bool:
        """
        Append one turn record to the JSONL file.

        Returns ``True`` if a record was written, ``False`` if collection is
        disabled. Never raises — the caller treats this as best-effort.
        """
        if not self.enabled:
            return False
        record = self.build_record(
            payload,
            player_action=player_action,
            latency_ms=latency_ms,
            evil_progress=evil_progress,
            ts=ts,
            turn_number=self._count + 1,
        )
        path = self._resolve_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._count += 1
        return True

    # --- introspection (tests + tooling) --------------------------------
    def count(self) -> int:
        """Number of records written by this collector instance."""
        return self._count

    def read_all(self) -> list[dict[str, Any]]:
        """Read every record back from the JSONL file (empty if none)."""
        path = self._resolve_path()
        if not path.exists():
            return []
        records: list[dict[str, Any]] = []
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records


_collector: Optional[DataCollector] = None


def get_collector() -> DataCollector:
    """Return the process-wide DataCollector singleton."""
    global _collector
    if _collector is None:
        _collector = DataCollector()
    return _collector


def reset_collector() -> None:
    """Clear the singleton (tests + config changes)."""
    global _collector
    _collector = None
