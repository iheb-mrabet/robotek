"""Simple fake mission logic for the mock robot."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from robot_mock.app.safety import SafetyValidationError, assert_safe_robot_profile


class MissionState(StrEnum):
    """Supported mock mission states."""

    IDLE = "IDLE"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class Waypoint:
    """A fake waypoint used by the mock mission."""

    name: str
    x: float
    y: float


@dataclass
class Mission:
    """A small in-memory mission state machine."""

    waypoints: list[Waypoint]
    state: MissionState = MissionState.IDLE
    current_index: int = -1
    failure_reason: str | None = None

    @classmethod
    def from_waypoints(cls, waypoints: list[dict[str, Any] | Waypoint]) -> Mission:
        parsed_waypoints = [_parse_waypoint(waypoint) for waypoint in waypoints]
        return cls(waypoints=parsed_waypoints)

    def start(self, profile: dict[str, Any], rules: dict[str, Any]) -> None:
        """Start a mission only when the robot profile is safe."""

        try:
            assert_safe_robot_profile(profile, rules)
        except SafetyValidationError as exc:
            self.state = MissionState.FAILED
            self.failure_reason = str(exc)
            raise

        if not self.waypoints:
            self.state = MissionState.FAILED
            self.failure_reason = "Mission requires at least one waypoint"
            raise ValueError(self.failure_reason)

        self.state = MissionState.RUNNING
        self.current_index = -1
        self.failure_reason = None

    def advance(self) -> MissionState:
        """Move to the next fake waypoint and complete when all are visited."""

        if self.state != MissionState.RUNNING:
            raise RuntimeError("Mission must be running before it can advance")

        self.current_index += 1
        if self.current_index >= len(self.waypoints):
            self.state = MissionState.COMPLETED
            self.current_index = len(self.waypoints) - 1

        return self.state

    def run_to_completion(self) -> MissionState:
        """Advance through all waypoints."""

        while self.state == MissionState.RUNNING:
            self.advance()
        return self.state

    def status(self) -> dict[str, Any]:
        """Return a serializable mission status."""

        current_waypoint = None
        if 0 <= self.current_index < len(self.waypoints):
            current_waypoint = self.waypoints[self.current_index].name

        return {
            "state": self.state.value,
            "current_waypoint": current_waypoint,
            "waypoints": [waypoint.name for waypoint in self.waypoints],
            "failure_reason": self.failure_reason,
        }


def create_mission_from_profile(profile: dict[str, Any]) -> Mission:
    """Create a mission from the default waypoints in a robot profile."""

    return Mission.from_waypoints(profile["default_mission_waypoints"])


def _parse_waypoint(waypoint: dict[str, Any] | Waypoint) -> Waypoint:
    if isinstance(waypoint, Waypoint):
        return waypoint

    return Waypoint(
        name=str(waypoint["name"]),
        x=float(waypoint["x"]),
        y=float(waypoint["y"]),
    )
