"""Prose streaming gate + Storyteller streaming (PR17)."""

from __future__ import annotations

from engine.agents.streaming import ProseStreamGate
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import GameState
from engine.agents.storyteller import StorytellerAgent


def _sink():
    out: list[str] = []
    return out, out.append


def test_gate_streams_prose_not_fenced_epilogue():
    chunks, sink = _sink()
    g = ProseStreamGate(sink)
    raw = (
        "The mist parts over the ferns. A crow watches.\n"
        '```json\n{"narration": "x", "choices": []}\n```'
    )
    for ch in raw:  # simulate token-by-token streaming
        g.feed(ch)
    g.flush()
    streamed = "".join(chunks)
    assert "json" not in streamed
    assert "{" not in streamed
    assert streamed.strip() == "The mist parts over the ferns. A crow watches."


def test_gate_unfenced_epilogue_boundary():
    chunks, sink = _sink()
    g = ProseStreamGate(sink)
    g.feed('You wake at the forest edge.\n{"narration": "", "choices": []}')
    g.flush()
    assert "".join(chunks).strip() == "You wake at the forest edge."


def test_gate_prose_only_emits_everything():
    chunks, sink = _sink()
    g = ProseStreamGate(sink)
    g.feed("Smoke drifts from a distant chimney.")
    g.flush()
    assert "".join(chunks) == "Smoke drifts from a distant chimney."


def test_gate_none_callback_is_safe():
    g = ProseStreamGate(None)
    g.feed("anything")
    g.flush()  # must not raise
    assert g.text == "anything"


def test_storyteller_streams_prose_via_on_delta():
    raw = (
        "The hearth smoke rises grey against the birches.\n"
        '```json\n{"narration": "The hearth smoke rises grey against the birches.",'
        ' "choices": [{"id": "a", "text": "Walk on"}], "tool_calls": []}\n```'
    )
    eng = GameEngine(GameState())
    set_active_engine(eng)
    chunks: list[str] = []
    st = StorytellerAgent(eng, llm_fn=lambda _m: raw)
    res = st.run_turn("look around", on_delta=chunks.append)

    streamed = "".join(chunks)
    assert "json" not in streamed and "{" not in streamed
    assert "hearth smoke" in streamed
    # the parsed result is unaffected by streaming
    assert res.narration == "The hearth smoke rises grey against the birches."
    assert res.choices[0]["text"] == "Walk on"


def test_storyteller_without_on_delta_unchanged():
    raw = '{"narration": "A quiet road.", "choices": [], "tool_calls": []}'
    eng = GameEngine(GameState())
    set_active_engine(eng)
    st = StorytellerAgent(eng, llm_fn=lambda _m: raw)
    res = st.run_turn("wait")  # no on_delta
    assert res.narration == "A quiet road."
