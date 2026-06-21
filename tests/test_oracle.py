"""Oracle turn telemetry + /api/metrics (PR30)."""

from __future__ import annotations

from engine.observability import Oracle, get_oracle, reset_oracle


def _payload(*, overall, passed, violations=0, spoke=False, intent="silent", gift=None, tools=0):
    return {
        "evaluation": {"overall": overall, "passed": passed},
        "governance": [{"rule_id": "R003"}] * violations,
        "assistant": {"spoke": spoke, "intent": intent, "gift": gift},
        "tool_receipts": [{}] * tools,
    }


def test_record_and_aggregate():
    o = Oracle()
    o.record_turn(_payload(overall=0.9, passed=True, tools=2), latency_ms=100, evil_progress=0.1)
    o.record_turn(_payload(overall=0.4, passed=False, violations=2), latency_ms=300, evil_progress=0.2)
    o.record_turn(_payload(overall=0.8, passed=True, spoke=True, intent="gift",
                           gift={"id": "bandage_poultice"}), latency_ms=200, evil_progress=0.3)
    m = o.metrics()
    assert m["turns"] == 3
    assert m["eval_pass_rate"] == round(2 / 3, 3)
    assert m["avg_eval"] == round((0.9 + 0.4 + 0.8) / 3, 3)
    assert m["violation_rate"] == round(1 / 3, 3)
    assert m["violations_total"] == 2
    assert m["assistant_intervention_rate"] == round(1 / 3, 3)
    assert m["gifts"] == 1
    assert m["avg_latency_ms"] == 200.0
    assert m["last_evil_progress"] == 0.3


def test_recent_ring():
    o = Oracle(ring=2)
    for i in range(3):
        o.record_turn(_payload(overall=0.5, passed=True), latency_ms=10)
    recent = o.recent(10)
    assert len(recent) == 2  # ring capped
    assert recent[-1]["turn"] == 3


def test_empty_metrics_safe():
    o = Oracle()
    m = o.metrics()
    assert m["turns"] == 0
    assert m["eval_pass_rate"] == 0.0


def test_metrics_endpoint():
    reset_oracle()
    from content.scenes.clockwork.clockwork_scene import create_app, reset_store

    reset_store()
    _, app = create_app(testing=True)
    get_oracle().record_turn(_payload(overall=0.7, passed=True), latency_ms=50, evil_progress=0.05)
    client = app.test_client()
    res = client.get("/api/metrics")
    assert res.status_code == 200
    data = res.get_json()
    assert data["metrics"]["turns"] >= 1
    assert isinstance(data["recent"], list)
    reset_oracle()
