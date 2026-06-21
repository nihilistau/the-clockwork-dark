"""
Inference Resilience & Turn Budget (PR18)
=========================================

A live local model is fallible: it drops connections, stalls, or loops on
retries. This module gives the agents three guards:

  * ``retry_call`` / ``@with_retries`` — exponential-backoff retry around a
    flaky inference call.
  * ``TurnBudget`` — a per-turn wall-clock + approx-token ceiling so a
    pathological retry loop can't burn unbounded compute.
  * ``approx_tokens`` — cheap chars/4 estimate (LM Studio omits token counts).

Version: v0.3.0 [2026-06-21]
"""

from __future__ import annotations

import functools
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def approx_tokens(text: str) -> int:
    """Rough token estimate (~4 chars/token) when the API gives no count."""
    return max(0, len(text or "") // 4)


@dataclass
class TurnBudget:
    """Wall-clock + approximate-token ceiling for a single turn.

    A value of 0 for either cap means "unlimited". ``exceeded()`` lets the
    Storyteller stop retrying once a turn has spent its allowance.
    """

    max_tokens: int = 0
    max_seconds: float = 0.0
    spent_tokens: int = 0
    _start: float = field(default_factory=time.perf_counter)

    def add_tokens(self, n: int) -> None:
        self.spent_tokens += max(0, int(n))

    def add_text(self, text: str) -> None:
        self.add_tokens(approx_tokens(text))

    def elapsed(self) -> float:
        return time.perf_counter() - self._start

    def exceeded(self) -> bool:
        if self.max_tokens and self.spent_tokens >= self.max_tokens:
            return True
        if self.max_seconds and self.elapsed() >= self.max_seconds:
            return True
        return False

    def reason(self) -> str:
        if self.max_tokens and self.spent_tokens >= self.max_tokens:
            return f"token budget {self.max_tokens} reached (~{self.spent_tokens})"
        if self.max_seconds and self.elapsed() >= self.max_seconds:
            return f"time budget {self.max_seconds}s reached ({self.elapsed():.1f}s)"
        return ""


def retry_call(
    fn: Callable[[], T],
    *,
    attempts: int = 2,
    base_delay: float = 0.4,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    sleep: Callable[[float], None] = time.sleep,
    log: Optional[logging.Logger] = None,
) -> T:
    """Call ``fn`` with exponential backoff; re-raise the last error if all fail."""
    n = max(1, attempts)
    last: Optional[BaseException] = None
    for i in range(n):
        try:
            return fn()
        except exceptions as exc:
            last = exc
            if log:
                log.warning(
                    "[resilience] attempt %d/%d failed: %s", i + 1, n, exc
                )
            if i < n - 1 and base_delay > 0:
                sleep(base_delay * (2 ** i))
    assert last is not None
    raise last


def with_retries(
    *,
    attempts: int = 2,
    base_delay: float = 0.4,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator form of :func:`retry_call`."""

    def deco(fn: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return retry_call(
                lambda: fn(*args, **kwargs),
                attempts=attempts,
                base_delay=base_delay,
                exceptions=exceptions,
                log=logger,
            )

        return wrapper

    return deco
