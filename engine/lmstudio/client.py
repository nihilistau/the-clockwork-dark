"""
LMSClient — LM Studio OpenAI-compatible SSE client.

Uses ``POST {base_url}/chat/completions`` with ``stream: true``.
Falls back gracefully when server is unavailable (for tests / offline dev).

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import json
import logging
import os
import time
import uuid
from typing import Any, Callable, Generator, Optional

import httpx

from engine.config import get_config
from engine.lmstudio.events import LMSResponse, LMSStreamEvent
from engine.lmstudio.profiles import ModelProfile, resolve_profile

logger = logging.getLogger(__name__)

_client_instance: Optional["LMSClient"] = None


class LMSClient:
    """HTTP client for LM Studio chat completions with SSE streaming."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        *,
        timeout: float = 120.0,
        api_key: str = "",
    ) -> None:
        cfg = get_config()
        self.base_url = (base_url or cfg.get("lmstudio.base_url", "http://localhost:1234/v1")).rstrip("/")
        self.timeout = timeout
        self.api_key = (
            api_key
            or cfg.get("lmstudio.api_key", "")
            or os.environ.get("LMSTUDIO_API_KEY", "")
            or ""
        )
        headers: dict[str, str] = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        self._client = httpx.Client(timeout=timeout, headers=headers)

    def close(self) -> None:
        """Close HTTP client."""
        self._client.close()

    def is_available(self) -> bool:
        """Return True if LM Studio responds."""
        try:
            r = self._client.get(f"{self.base_url}/models", timeout=3.0)
            return r.status_code == 200
        except Exception as exc:
            logger.debug("[LMSClient] Health check failed (operation=health): %s", exc)
            return False

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: float = 0.8,
        max_tokens: int = 1500,
    ) -> LMSResponse:
        """Non-streaming chat completion."""
        chunks: list[str] = []
        for chunk in self.chat_stream(
            messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            chunks.append(chunk)
        return LMSResponse(content="".join(chunks), model=model or "")

    def chat_stream(
        self,
        messages: list[dict[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: float = 0.8,
        max_tokens: int = 1500,
        on_event: Optional[Callable[[LMSStreamEvent], None]] = None,
    ) -> Generator[str, None, LMSResponse]:
        """
        Stream chat completion tokens.

        Yields content deltas. Fires typed LMSStreamEvent via on_event.
        """
        resolved = model or resolve_profile("big").model
        payload = {
            "model": resolved,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        t0 = time.perf_counter()
        if on_event:
            on_event(LMSStreamEvent(event_type="chat.start", model_instance_id=resolved))

        content_parts: list[str] = []
        try:
            with self._client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=self.timeout,
            ) as response:
                response.raise_for_status()
                for raw_line in response.iter_lines():
                    line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line
                    if not line or not line.startswith("data:"):
                        continue
                    data_str = line[5:].strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                    except json.JSONDecodeError:
                        continue
                    delta = (
                        data.get("choices", [{}])[0]
                        .get("delta", {})
                        .get("content", "")
                    )
                    if delta:
                        content_parts.append(delta)
                        if on_event:
                            on_event(
                                LMSStreamEvent(
                                    event_type="message.delta",
                                    content=delta,
                                )
                            )
                        yield delta
        except httpx.HTTPError as exc:
            logger.error("[LMSClient] Stream failed (operation=chat_stream): %s", exc)
            if on_event:
                on_event(LMSStreamEvent(event_type="error", error=str(exc)))
            raise

        full = "".join(content_parts)
        latency = (time.perf_counter() - t0) * 1000
        if on_event:
            on_event(
                LMSStreamEvent(
                    event_type="chat.end",
                    response_id=f"resp_{uuid.uuid4().hex[:12]}",
                    stats={"latency_ms": latency},
                )
            )
        return LMSResponse(content=full, model=resolved, latency_ms=latency)

    def infer_stream(
        self,
        messages: list[dict[str, Any]],
        *,
        profile: str = "big",
        on_event: Optional[Callable[[LMSStreamEvent], None]] = None,
    ) -> Generator[str, None, LMSResponse]:
        """Profile-aware streaming wrapper."""
        mp = resolve_profile(profile)
        return self.chat_stream(
            messages,
            model=mp.model,
            temperature=mp.temperature,
            max_tokens=mp.max_tokens,
            on_event=on_event,
        )

    def infer_processed(
        self,
        messages: list[dict[str, Any]],
        *,
        profile: str = "big",
        on_delta: Optional[Callable[[str], None]] = None,
    ):
        """
        Stream + tag extraction via StreamProcessor.

        Returns:
            ProcessedResponse from engine.agents.stream_processor
        """
        from engine.agents.stream_processor import StreamProcessor

        proc = StreamProcessor(on_delta=on_delta)
        gen = self.infer_stream(messages, profile=profile, on_event=proc.on_event)
        for _chunk in gen:
            pass
        return proc.result()


def get_lms_client() -> LMSClient:
    """Singleton LMS client."""
    global _client_instance
    if _client_instance is None:
        _client_instance = LMSClient()
    return _client_instance


def reset_lms_client() -> None:
    """Reset singleton (tests)."""
    global _client_instance
    if _client_instance is not None:
        _client_instance.close()
    _client_instance = None