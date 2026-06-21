"""
TTS Client
==========

Text-to-speech via HTTP service with text-only fallback.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import logging
from typing import Any, Optional

import httpx

from engine.config import get_config
from engine.media.queue import MediaJob, get_media_queue

logger = logging.getLogger(__name__)


class TTSClient:
    """
    Synthesize narration audio via configured TTS endpoint.

    Falls back to text-only when service is unavailable.
    """

    def __init__(self, base_url: Optional[str] = None) -> None:
        cfg = get_config()
        self.base_url = (base_url or cfg.get("tts.base_url", "http://localhost:8600")).rstrip(
            "/"
        )
        self.fallback = str(cfg.get("tts.fallback", "text"))
        self.timeout = float(cfg.get("tts.timeout_seconds", 60))

    def synthesize(
        self,
        text: str,
        *,
        voice: str = "storyteller",
        style: str = "",
    ) -> dict[str, Any]:
        """
        Synthesize speech for narration line.

        Args:
            text: Line to speak.
            voice: Voice profile id.
            style: Optional style hint (whisper, urgent).

        Returns:
            Dict with audio_url or text-only fallback.
        """
        if not text.strip():
            return {"success": False, "source": "empty", "text": ""}

        url = f"{self.base_url}/v1/audio/speech"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    url,
                    json={"input": text, "voice": voice, "style": style},
                )
                response.raise_for_status()
                content_type = response.headers.get("content-type", "")
                if "audio" in content_type:
                    return {
                        "success": True,
                        "source": "live",
                        "audio_bytes": response.content,
                        "content_type": content_type,
                        "text": text,
                    }
                data = response.json()
                return {
                    "success": True,
                    "source": "live",
                    "audio_url": data.get("url", ""),
                    "text": text,
                }
        except Exception as exc:
            logger.warning("[tts] Service unavailable (operation=synthesize): %s", exc)
            return {
                "success": False,
                "source": self.fallback,
                "text": text,
                "message": str(exc),
            }

    def enqueue_narration(
        self,
        text: str,
        *,
        voice: str = "storyteller",
        style: str = "",
    ) -> MediaJob:
        """Queue a TTS job for narration."""
        queue = get_media_queue()
        result = self.synthesize(text, voice=voice, style=style)
        job = MediaJob(
            job_id=queue.new_job_id(),
            kind="tts",
            cache_key="",
            prompt=text,
            payload={"voice": voice, "style": style, "result": result},
            status="ready" if result.get("success") else "fallback",
            url=str(result.get("audio_url", "")),
        )
        return queue.enqueue(job)