"""
Prose Stream Gate (PR17)
========================

The Storyteller streams narration prose followed by a ```json {...} epilogue.
We want the *prose* to flow to the client live (so a turn doesn't freeze for the
whole LLM latency) but we must NOT leak the JSON epilogue into the narrative log.

``ProseStreamGate`` forwards prose deltas to ``on_delta`` and stops at the
epilogue boundary, holding back a short tail so a partially-arrived code fence
isn't emitted character-by-character.

Version: v0.3.0 [2026-06-21]
"""

from __future__ import annotations

from typing import Callable, Optional


class ProseStreamGate:
    """Stream the narration prose that precedes the JSON epilogue."""

    _HOLD = 4  # hold back a few chars so a forming "```" / "```j" isn't emitted

    def __init__(self, on_delta: Optional[Callable[[str], None]]) -> None:
        self._on_delta = on_delta
        self._buf = ""
        self._sent = 0
        self._gated = False

    @property
    def text(self) -> str:
        """Everything fed so far (prose + epilogue)."""
        return self._buf

    def feed(self, chunk: str) -> None:
        """Accumulate a delta and forward any safe prose to ``on_delta``."""
        if not chunk:
            return
        self._buf += chunk
        if self._gated or self._on_delta is None:
            return
        boundary = self._boundary(self._buf)
        if boundary is not None:
            if boundary > self._sent:
                self._emit(self._buf[self._sent:boundary])
                self._sent = boundary
            self._gated = True
            return
        safe = len(self._buf) - self._HOLD
        if safe > self._sent:
            self._emit(self._buf[self._sent:safe])
            self._sent = safe

    def flush(self) -> None:
        """Emit remaining prose up to the epilogue boundary, then close."""
        if self._gated or self._on_delta is None:
            self._gated = True
            return
        boundary = self._boundary(self._buf)
        end = boundary if boundary is not None else len(self._buf)
        if end > self._sent:
            self._emit(self._buf[self._sent:end])
            self._sent = end
        self._gated = True

    @staticmethod
    def _boundary(text: str) -> Optional[int]:
        cands = [i for i in (text.find("```"), text.find("\n{")) if i != -1]
        return min(cands) if cands else None

    def _emit(self, text: str) -> None:
        if text and self._on_delta is not None:
            try:
                self._on_delta(text)
            except Exception:
                pass  # a flaky client callback must never break a turn
