"""
Scheduler — deterministic cadence runner.
=========================================

A tiny, in-memory scheduler for world-tick and maintenance cadence. It owns **no
threads and no real clock** — the caller injects ``now`` on every ``tick`` — so
it is fully deterministic and unit-testable. The host loop decides when to call
``tick(now)`` (e.g. once per request, or from a background loop); the scheduler
only answers "which tasks are due, and run them."

This mirrors the engine rule that timing must be injectable, not wall-clock
bound (see ``WorldSim.should_run_realtime_tick(now=...)``).

    sched = Scheduler()
    sched.add_task("world_tick", 60.0, run_world_tick)
    sched.tick(now=0.0)     # -> ["world_tick"]  (first run fires immediately)
    sched.tick(now=30.0)    # -> []              (interval not elapsed)
    sched.tick(now=61.0)    # -> ["world_tick"]  (elapsed since last run)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable

logger = logging.getLogger(__name__)


@dataclass
class _Task:
    name: str
    interval_seconds: float
    fn: Callable[[], object]
    last_run: float = field(default=float("-inf"))


class Scheduler:
    """In-memory, clock-injected task scheduler (no real threads)."""

    def __init__(self) -> None:
        self._tasks: dict[str, _Task] = {}

    def add_task(
        self,
        name: str,
        interval_seconds: float,
        fn: Callable[[], object],
    ) -> None:
        """
        Register (or replace) a task to run at most once per interval.

        A task is considered due immediately on its first ``tick`` (it has never
        run), then again once ``interval_seconds`` have elapsed since its last run.
        """
        if interval_seconds < 0:
            raise ValueError("interval_seconds must be >= 0")
        self._tasks[name] = _Task(name=name, interval_seconds=float(interval_seconds), fn=fn)

    def remove_task(self, name: str) -> None:
        """Drop a task by name (no-op if absent)."""
        self._tasks.pop(name, None)

    def tasks(self) -> list[str]:
        """Registered task names (insertion order)."""
        return list(self._tasks.keys())

    def due(self, now: float) -> list[str]:
        """Names of tasks whose interval has elapsed at ``now`` (does not run)."""
        return [
            t.name
            for t in self._tasks.values()
            if (now - t.last_run) >= t.interval_seconds
        ]

    def tick(self, now: float) -> list[str]:
        """
        Run every due task, marking it run at ``now``. Returns the names run, in
        registration order. A failing task is logged and skipped — one bad task
        never blocks the others (never breaks a turn).
        """
        ran: list[str] = []
        for name in self.due(now):
            task = self._tasks[name]
            try:
                task.fn()
            except Exception:  # pragma: no cover - defensive, fail-safe
                logger.exception("[scheduler] Task failed (name=%s)", name)
            task.last_run = now
            ran.append(name)
        return ran
