"""Fake health/status reporting for the mock robot."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from robot_mock.app.mission import MissionState


def get_robot_health(
    mission_state: MissionState | str = MissionState.IDLE,
    profile: dict[str, Any] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Return deterministic-enough fake robot health for tests and local use."""

    timestamp = now or datetime.now(UTC)
    emergency_stop_enabled = True
    if profile is not None:
        emergency_stop_enabled = bool(profile.get("emergency_stop_enabled", True))

    state_value = mission_state.value if isinstance(mission_state, MissionState) else mission_state

    return {
        "service_status": "OK",
        "battery_percentage": 87,
        "emergency_stop_state": "enabled" if emergency_stop_enabled else "disabled",
        "mission_state": state_value,
        "timestamp": timestamp.isoformat(),
    }
