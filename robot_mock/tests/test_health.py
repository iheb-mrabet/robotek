from __future__ import annotations

from datetime import UTC, datetime

from robot_mock.app.health import get_robot_health
from robot_mock.app.mission import MissionState


def test_health_status_contains_expected_fields() -> None:
    health = get_robot_health(
        mission_state=MissionState.RUNNING,
        now=datetime(2026, 1, 1, tzinfo=UTC),
    )

    assert set(health) == {
        "service_status",
        "battery_percentage",
        "emergency_stop_state",
        "mission_state",
        "timestamp",
    }
    assert health["mission_state"] == "RUNNING"
    assert health["timestamp"] == "2026-01-01T00:00:00+00:00"


def test_battery_value_is_between_0_and_100() -> None:
    health = get_robot_health()

    assert 0 <= health["battery_percentage"] <= 100


def test_service_status_is_ok() -> None:
    health = get_robot_health()

    assert health["service_status"] == "OK"
