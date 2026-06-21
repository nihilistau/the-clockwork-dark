"""
Training — self-improvement plumbing.
=====================================

Two small, deterministic, testable pieces that feed future fine-tuning without
ever touching the hard engine or breaking a turn:

- ``DataCollector`` — appends one JSONL record per turn (gated by
  ``training.collect``, default off) for later supervised fine-tuning.
- ``Scheduler`` — an in-memory, clock-injected cadence runner for world-tick /
  maintenance tasks (no real threads; unit-testable).
"""

from engine.training.data_collector import (
    DataCollector,
    get_collector,
    reset_collector,
)
from engine.training.scheduler import Scheduler

__all__ = [
    "DataCollector",
    "get_collector",
    "reset_collector",
    "Scheduler",
]
