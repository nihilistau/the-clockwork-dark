"""Media pipeline tests — ComfyUI queue, TTS fallback, cutscene budget."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from engine.game.engine import GameEngine
from engine.game.procgen import new_game_state
from engine.game.state import EvilPhase
from engine.media.comfyui import ComfyUIClient, build_image_prompt, load_comfyui_templates
from engine.media.cutscene import CutsceneBudget, CutsceneRunner
from engine.media.interceptors import run_media_interceptors
from engine.media.pipeline import MediaPipeline
from engine.media.queue import make_cache_key, parse_image_tag, reset_media_queue
from engine.media.tts import TTSClient


def _engine() -> GameEngine:
    return GameEngine(new_game_state(seed=42))


def test_parse_image_tag():
    assert parse_image_tag("forest_clearing_dawn") == ("forest_clearing", "dawn")
    assert parse_image_tag("edgewood_square") == ("edgewood_square", "dawn")


def test_cache_key_stable():
    a = make_cache_key("forest_clearing", "dawn", "dormant")
    b = make_cache_key("forest_clearing", "dawn", "dormant")
    assert a == b
    assert a != make_cache_key("forest_clearing", "noon", "dormant")


def test_build_image_prompt():
    prompt = build_image_prompt("forest_clearing_dawn", evil_phase="dormant")
    assert "birch" in prompt.lower()
    assert "oil-painted" in prompt


def test_comfyui_enqueue_placeholder():
    reset_media_queue()
    engine = _engine()
    client = ComfyUIClient()
    job = client.enqueue_image("forest_clearing_dawn", engine.state)
    assert job.kind == "image"
    assert job.status == "placeholder"
    assert "/design/" in job.url or "forest_clearing_dawn" in job.url
    from engine.media.queue import get_media_queue

    assert len(get_media_queue().all_jobs()) == 1
    assert job.cache_key in engine.state.media_cache


def test_comfyui_cache_hit():
    reset_media_queue()
    engine = _engine()
    client = ComfyUIClient()
    first = client.enqueue_image("edgewood_square_dawn", engine.state)
    reset_media_queue()
    second = client.enqueue_image("edgewood_square_dawn", engine.state)
    assert second.status == "cached"
    assert second.url == first.url


def test_tts_fallback():
    client = TTSClient(base_url="http://127.0.0.1:1")
    result = client.synthesize("The mist lingers.")
    assert result["success"] is False
    assert result["source"] == "text"
    assert result["text"] == "The mist lingers."


def test_cutscene_budget_blocks_second_in_phase():
    engine = _engine()
    engine.state.evil_phase = EvilPhase.STIRRING
    runner = CutsceneRunner()
    first = runner.enqueue_cutscene("cutscene_stirring_phase", engine.state)
    second = runner.enqueue_cutscene("cutscene_assistant_reveal", engine.state)
    assert first is not None
    assert second is None


def test_cutscene_budget_resets_on_phase_shift():
    engine = _engine()
    engine.state.evil_phase = EvilPhase.STIRRING
    runner = CutsceneRunner()
    runner.enqueue_cutscene("cutscene_stirring_phase", engine.state)
    engine.state.evil_phase = EvilPhase.SPREADING
    allowed = runner.enqueue_cutscene("cutscene_consuming_horizon", engine.state)
    assert allowed is not None


def test_media_pipeline_process_tags():
    reset_media_queue()
    engine = _engine()
    pipe = MediaPipeline()
    result = pipe.process_tags(
        engine.state,
        image_tags=["forest_clearing_dawn"],
        cutscene_tags=["cutscene_stirring_phase"],
        narration="Smoke rises from Edgewood.",
        force_cutscenes=True,
    )
    assert len(result.images) == 1
    assert len(result.cutscenes) == 1
    assert len(result.tts_jobs) == 1


def test_run_media_interceptors():
    reset_media_queue()
    engine = _engine()
    data = run_media_interceptors(
        engine.state,
        narration="A cold morning.",
        processed_tags={"image": ["forest_clearing_dawn"]},
    )
    assert len(data["images"]) == 1
    assert data["tts_jobs"]


def test_comfyui_submit_when_enabled():
    reset_media_queue()
    engine = _engine()
    client = ComfyUIClient()
    client.enabled = True

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"prompt_id": "abc123"}

    with patch("httpx.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.__enter__.return_value = mock_client
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        job = client.enqueue_image("edgewood_square_noon", engine.state)
        assert job.status == "submitted"
        assert job.payload["comfyui"]["prompt_id"] == "abc123"
        mock_client.post.assert_called_once()


def test_comfyui_templates_load():
    tpl = load_comfyui_templates()
    assert "forest_clearing" in tpl.get("locations", {})
    assert "cutscene_stirring_phase" in tpl.get("cutscenes", {})