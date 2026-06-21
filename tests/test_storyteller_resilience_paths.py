"""Storyteller resilience + required-tool-failure gating.

Two gaps:
  * transport failure at the *client* level exhausts ``retry_call`` and the
    Storyteller falls back to ``fallback_narration`` (not just an injected
    ``llm_fn`` raiser, but the real chat-client error path);
  * a REQUIRED skill receipt with ``success=False`` (an illegal ``move_to``)
    caps mechanics in the Evaluator and the turn does NOT pass.
"""

from __future__ import annotations

import json

import httpx

from engine.agents.storyteller import StorytellerAgent
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import GameState


class _AlwaysFailsClient:
    """Stand-in LMS client whose stream/chat always raise a transport error."""

    def __init__(self) -> None:
        self.calls = 0

    def chat_stream(self, *_a, **_k):
        self.calls += 1
        raise httpx.ConnectError("LM Studio unreachable")
        yield  # pragma: no cover - generator marker, never reached

    def chat(self, *_a, **_k):
        self.calls += 1
        raise httpx.ConnectError("LM Studio unreachable")


def test_storyteller_falls_back_after_retries_exhaust():
    eng = GameEngine(GameState())
    set_active_engine(eng)
    client = _AlwaysFailsClient()
    st = StorytellerAgent(eng, lms_client=client)
    st._infer_backoff = 0.0  # no real sleeping in tests

    res = st.run_turn("look around")

    assert res.narration == st._fallback_narration
    # retry_call must have actually retried before giving up
    assert client.calls >= st._infer_attempts


def test_required_tool_failure_fails_the_turn():
    # From forest_clearing there is no edge to millhaven_gate -> move_to fails.
    state = GameState(location_id="forest_clearing")
    eng = GameEngine(state)

    payload = {
        "tool_calls": [{"name": "move_to", "args": {"location_id": "millhaven_gate"}}],
        "narration": (
            "You set off down the road toward the distant gate, boots loud on the "
            "frosted ruts, the mist closing grey behind you as the village falls away."
        ),
        "choices": [{"id": "a", "text": "Keep walking"}, {"id": "b", "text": "Turn back"}],
        "skill_check": None,
    }

    st = StorytellerAgent(eng, llm_fn=lambda _m: f"```json\n{json.dumps(payload)}\n```")
    res = st.run_turn("Walk to the militia gate.")

    # the required move receipt failed
    move = next(r for r in res.tool_receipts if r["skill"] == "move_to")
    assert move["success"] is False
    # Evaluator caps mechanics and the turn does not pass
    assert res.evaluation.no_hallucinated_mechanics <= 0.4
    assert res.evaluation.passed is False
    assert any("failed" in n.lower() for n in res.evaluation.notes)
    # the player never actually moved
    assert state.location_id == "forest_clearing"
