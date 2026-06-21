"""Native structured output (response_format) wiring (PR23)."""

from __future__ import annotations

import json

import httpx

from engine.agents.schemas import STORYTELLER_RESPONSE_FORMAT, STORYTELLER_SCHEMA
from engine.lmstudio.client import LMSClient


def test_schema_shape():
    assert STORYTELLER_RESPONSE_FORMAT["type"] == "json_schema"
    js = STORYTELLER_RESPONSE_FORMAT["json_schema"]
    assert js["name"] == "clockwork_turn"
    assert js["schema"] is STORYTELLER_SCHEMA
    assert "narration" in STORYTELLER_SCHEMA["properties"]
    assert STORYTELLER_SCHEMA["required"] == ["narration", "choices"]


def _mock_client(capture: dict) -> LMSClient:
    def handler(request: httpx.Request) -> httpx.Response:
        capture["body"] = json.loads(request.content)
        body = (
            'data: {"choices":[{"delta":{"content":"hi"}}]}\n\n'
            "data: [DONE]\n\n"
        )
        return httpx.Response(200, text=body)

    client = LMSClient(base_url="http://test/v1")
    client._client = httpx.Client(transport=httpx.MockTransport(handler))
    return client


def test_chat_includes_response_format_in_payload():
    capture: dict = {}
    client = _mock_client(capture)
    out = client.chat(
        [{"role": "user", "content": "hi"}],
        model="m",
        response_format=STORYTELLER_RESPONSE_FORMAT,
    )
    assert out.content == "hi"
    assert capture["body"]["response_format"] == STORYTELLER_RESPONSE_FORMAT


def test_chat_omits_response_format_when_none():
    capture: dict = {}
    client = _mock_client(capture)
    client.chat([{"role": "user", "content": "hi"}], model="m")
    assert "response_format" not in capture["body"]


def test_storyteller_structured_flag_default_off():
    from engine.game.engine import GameEngine, set_active_engine
    from engine.game.state import GameState
    from engine.agents.storyteller import StorytellerAgent

    eng = GameEngine(GameState())
    set_active_engine(eng)
    st = StorytellerAgent(eng, llm_fn=lambda _m: '{"narration":"x","choices":[]}')
    assert st._structured is False  # default; opt-in via config
    # a turn still resolves with the mock regardless of structured mode
    res = st.run_turn("look")
    assert res.narration == "x"
