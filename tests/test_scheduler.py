"""Scheduler — deterministic, clock-injected cadence runner."""

from __future__ import annotations

import pytest

from engine.training import Scheduler


def test_first_tick_runs_immediately():
    sched = Scheduler()
    calls = []
    sched.add_task("world_tick", 60.0, lambda: calls.append("ran"))
    assert sched.tick(now=0.0) == ["world_tick"]
    assert calls == ["ran"]


def test_interval_gating_is_deterministic():
    sched = Scheduler()
    runs = []
    sched.add_task("world_tick", 60.0, lambda: runs.append(True))

    assert sched.tick(now=0.0) == ["world_tick"]   # first run fires
    assert sched.tick(now=30.0) == []              # not yet elapsed
    assert sched.tick(now=59.9) == []              # still not elapsed
    assert sched.tick(now=60.0) == ["world_tick"]  # exactly elapsed -> runs
    assert sched.tick(now=61.0) == []              # just ran
    assert sched.tick(now=120.0) == ["world_tick"] # elapsed again
    assert len(runs) == 3


def test_due_does_not_run():
    sched = Scheduler()
    calls = []
    sched.add_task("t", 10.0, lambda: calls.append(1))
    assert sched.due(now=0.0) == ["t"]
    assert calls == []  # due() is a query, not a run
    assert sched.tick(now=0.0) == ["t"]
    assert calls == [1]


def test_multiple_tasks_independent_cadence():
    sched = Scheduler()
    fast, slow = [], []
    sched.add_task("fast", 10.0, lambda: fast.append(1))
    sched.add_task("slow", 100.0, lambda: slow.append(1))

    assert set(sched.tick(now=0.0)) == {"fast", "slow"}
    assert sched.tick(now=10.0) == ["fast"]        # only fast is due
    assert sched.tick(now=20.0) == ["fast"]
    assert set(sched.tick(now=100.0)) == {"fast", "slow"}
    assert len(fast) == 4
    assert len(slow) == 2


def test_add_task_replaces_and_resets():
    sched = Scheduler()
    a, b = [], []
    sched.add_task("job", 50.0, lambda: a.append(1))
    sched.tick(now=0.0)
    sched.add_task("job", 50.0, lambda: b.append(1))  # replace -> fresh last_run
    assert sched.tick(now=1.0) == ["job"]
    assert a == [1] and b == [1]


def test_remove_task():
    sched = Scheduler()
    sched.add_task("job", 10.0, lambda: None)
    assert "job" in sched.tasks()
    sched.remove_task("job")
    assert sched.tasks() == []
    assert sched.tick(now=999.0) == []


def test_zero_interval_runs_every_tick():
    sched = Scheduler()
    n = []
    sched.add_task("hot", 0.0, lambda: n.append(1))
    assert sched.tick(now=0.0) == ["hot"]
    assert sched.tick(now=0.0) == ["hot"]
    assert len(n) == 2


def test_negative_interval_rejected():
    sched = Scheduler()
    with pytest.raises(ValueError):
        sched.add_task("bad", -1.0, lambda: None)


def test_failing_task_does_not_block_others():
    sched = Scheduler()
    ok = []

    def boom():
        raise RuntimeError("nope")

    sched.add_task("boom", 10.0, boom)
    sched.add_task("ok", 10.0, lambda: ok.append(1))
    ran = sched.tick(now=0.0)
    assert set(ran) == {"boom", "ok"}  # both marked run, no exception escapes
    assert ok == [1]
