"""World simulation — ticks, schedules, trader events."""

from engine.world.schedules import ScheduleRoll, SimEvent

__all__ = ["WorldSim", "ScheduleRoll", "SimEvent"]


def __getattr__(name: str):
    if name == "WorldSim":
        from engine.world.world_sim import WorldSim

        return WorldSim
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")