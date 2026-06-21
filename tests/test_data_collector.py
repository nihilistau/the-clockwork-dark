"""DataCollector — gated turn capture to JSONL (self-improvement plumbing)."""

from __future__ import annotations

import pytest

from engine.config import get_config
from engine.training import DataCollector, get_collector, reset_collector


def _payload(**over):
    base = {
        "session_id": "sess-1",
        "narration": "The road waits.",
        "choices": [{"id": "a"}, {"id": "b"}],
        "tool_receipts": [
            {"skill": "roll_dice", "result": {"success": True}},
            {"skill": "move_to", "success": False},
        ],
        "evaluation": {"overall": 0.85, "passed": True},
        "governance": [{"rule_id": "R003"}],
        "assistant": {"spoke": True, "intent": "hint", "gift": {"id": "candle"}},
        "doom": {"arc": "whisper", "progress": 0.2},
    }
    base.update(over)
    return base


@pytest.fixture
def collect_to_tmp(tmp_path, monkeypatch):
    """Enable collection and point training data at a tmp JSONL; reset singleton."""
    cfg = get_config()
    monkeypatch.setitem(cfg._data, "training", {"collect": True})
    out = tmp_path / "turns.jsonl"
    monkeypatch.setitem(cfg._data, "paths", {**cfg._data.get("paths", {}), "training_data": str(out)})
    reset_collector()
    yield out
    reset_collector()


def test_writes_and_reads_jsonl_when_enabled(collect_to_tmp):
    out = collect_to_tmp
    c = get_collector()
    wrote = c.record(
        _payload(),
        player_action="The player chooses to follow the smoke",
        latency_ms=123.45,
        evil_progress=0.07,
        ts=1000.0,
    )
    assert wrote is True
    assert out.exists()
    assert c.count() == 1

    records = c.read_all()
    assert len(records) == 1
    rec = records[0]
    assert rec["session_id"] == "sess-1"
    assert rec["turn_number"] == 1
    assert rec["player_action"] == "The player chooses to follow the smoke"
    assert rec["narration"] == "The road waits."
    assert rec["choices"] == 2
    assert rec["tool_receipts"] == [
        {"skill": "roll_dice", "success": True},
        {"skill": "move_to", "success": False},
    ]
    assert rec["evaluation"] == {"overall": 0.85, "passed": True}
    assert rec["governance"] == 1
    assert rec["assistant"] == {"spoke": True, "intent": "hint", "gift": True}
    assert rec["doom"] == {"arc": "whisper", "progress": 0.2}
    assert rec["evil_progress"] == 0.07
    assert rec["latency_ms"] == 123.5
    assert rec["ts"] == 1000.0


def test_appends_multiple_turns(collect_to_tmp):
    c = get_collector()
    c.record(_payload(), ts=1.0)
    c.record(_payload(), ts=2.0)
    records = c.read_all()
    assert [r["turn_number"] for r in records] == [1, 2]
    assert c.count() == 2


def test_noop_when_disabled(tmp_path, monkeypatch):
    cfg = get_config()
    monkeypatch.setitem(cfg._data, "training", {"collect": False})
    out = tmp_path / "turns.jsonl"
    monkeypatch.setitem(cfg._data, "paths", {**cfg._data.get("paths", {}), "training_data": str(out)})
    reset_collector()
    try:
        c = get_collector()
        wrote = c.record(_payload(), player_action="x", latency_ms=5.0)
        assert wrote is False
        assert c.count() == 0
        assert not out.exists()
        assert c.read_all() == []
    finally:
        reset_collector()


def test_default_collect_is_off():
    # The shipped config must never collect by default (CI writes nothing).
    assert bool(get_config().get("training.collect", False)) is False


def test_build_record_is_pure_and_safe():
    # Missing/odd fields degrade gracefully without raising.
    rec = DataCollector.build_record({}, player_action="", latency_ms=0.0, ts=42.0)
    assert rec["session_id"] == ""
    assert rec["choices"] == 0
    assert rec["tool_receipts"] == []
    assert rec["evaluation"] == {"overall": 0.0, "passed": False}
    assert rec["governance"] == 0
    assert rec["assistant"] == {"spoke": False, "intent": "silent", "gift": False}
    assert rec["doom"] is None
    assert rec["ts"] == 42.0
