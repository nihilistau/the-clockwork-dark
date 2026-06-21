"""
Media Pipeline
==============

Process StreamProcessor tags into queued media jobs.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from engine.game.state import GameState
from engine.media.comfyui import ComfyUIClient
from engine.media.cutscene import CutsceneRunner
from engine.media.queue import MediaJob
from engine.media.tts import TTSClient


@dataclass
class MediaPipelineResult:
    """Jobs produced from a turn's media tags."""

    images: list[MediaJob] = field(default_factory=list)
    cutscenes: list[MediaJob] = field(default_factory=list)
    tts_jobs: list[MediaJob] = field(default_factory=list)
    blocked_cutscenes: list[str] = field(default_factory=list)

    def all_jobs(self) -> list[MediaJob]:
        return [*self.images, *self.cutscenes, *self.tts_jobs]

    def to_dict(self) -> dict[str, Any]:
        return {
            "images": [j.to_dict() for j in self.images],
            "cutscenes": [j.to_dict() for j in self.cutscenes],
            "tts_jobs": [j.to_dict() for j in self.tts_jobs],
            "blocked_cutscenes": list(self.blocked_cutscenes),
        }


class MediaPipeline:
    """
    POST-phase media processor for Storyteller output.

    Mirrors ComfyUIMediaInterceptor + TTSInterceptor + CutsceneBudgetInterceptor.
    """

    def __init__(
        self,
        *,
        comfyui: Optional[ComfyUIClient] = None,
        tts: Optional[TTSClient] = None,
        cutscenes: Optional[CutsceneRunner] = None,
    ) -> None:
        self._comfyui = comfyui or ComfyUIClient()
        self._tts = tts or TTSClient()
        self._cutscenes = cutscenes or CutsceneRunner()

    def process_tags(
        self,
        state: GameState,
        *,
        image_tags: Optional[list[str]] = None,
        cutscene_tags: Optional[list[str]] = None,
        narration: str = "",
        voice_style: str = "",
        queue_tts: bool = True,
        force_cutscenes: bool = False,
    ) -> MediaPipelineResult:
        """
        Enqueue media jobs from processed stream tags.

        Args:
            state: Session state.
            image_tags: [IMAGE:] ids from StreamProcessor.
            cutscene_tags: [CUTSCENE:] ids.
            narration: Storyteller narration for TTS.
            voice_style: TTS style hint.
            queue_tts: Whether to enqueue narration TTS.
            force_cutscenes: Bypass cutscene budget (tests).

        Returns:
            MediaPipelineResult with queued jobs.
        """
        result = MediaPipelineResult()
        for tag in image_tags or []:
            job = self._comfyui.enqueue_image(tag, state)
            result.images.append(job)

        for cid in cutscene_tags or []:
            job = self._cutscenes.enqueue_cutscene(
                cid,
                state,
                force=force_cutscenes,
            )
            if job:
                result.cutscenes.append(job)
            else:
                result.blocked_cutscenes.append(cid)

        if queue_tts and narration.strip():
            job = self._tts.enqueue_narration(
                narration,
                voice="storyteller",
                style=voice_style,
            )
            result.tts_jobs.append(job)

        return result

    def process_storyteller_turn(
        self,
        state: GameState,
        *,
        narration: str,
        processed_tags: dict[str, list[str]],
        voice_style: str = "",
    ) -> MediaPipelineResult:
        """Convenience wrapper for StorytellerTurnResult.processed_tags."""
        return self.process_tags(
            state,
            image_tags=processed_tags.get("image"),
            cutscene_tags=processed_tags.get("cutscene"),
            narration=narration,
            voice_style=voice_style,
        )