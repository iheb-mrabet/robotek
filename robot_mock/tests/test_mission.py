from __future__ import annotations

import pytest

from robot_mock.app.mission import Mission, MissionState, create_mission_from_profile
from robot_mock.app.safety import SafetyValidationError


@pytest.fixture
def safe_profile() -> dict[str, object]:
    return {
        "robot_name": "mock-rover-01",
        "environment": "staging",
        "max_speed_mps": 1.0,
        "debug": False,
        "emergency_stop_enabled": True,
        "default_mission_waypoints": [
            {"name": "dock", "x": 0.0, "y": 0.0},
            {"name": "inspection", "x": 1.0, "y": 1.0},
        ],
    }


@pytest.fixture
def safety_rules() -> dict[str, object]:
    return {
        "max_allowed_speed_mps": 1.5,
        "require_emergency_stop": True,
        "forbid_debug_in": ["staging", "production"],
    }


def test_mission_can_be_created(safe_profile: dict[str, object]) -> None:
    mission = create_mission_from_profile(safe_profile)

    assert mission.state == MissionState.IDLE
    assert [waypoint.name for waypoint in mission.waypoints] == ["dock", "inspection"]


def test_mission_starts_only_with_safe_config(
    safe_profile: dict[str, object],
    safety_rules: dict[str, object],
) -> None:
    mission = create_mission_from_profile(safe_profile)

    mission.start(safe_profile, safety_rules)

    assert mission.state == MissionState.RUNNING


def test_mission_rejects_unsafe_config(
    safe_profile: dict[str, object],
    safety_rules: dict[str, object],
) -> None:
    unsafe_profile = safe_profile | {"emergency_stop_enabled": False}
    mission = create_mission_from_profile(unsafe_profile)

    with pytest.raises(SafetyValidationError):
        mission.start(unsafe_profile, safety_rules)

    assert mission.state == MissionState.FAILED


def test_mission_completes_after_moving_through_waypoints(
    safe_profile: dict[str, object],
    safety_rules: dict[str, object],
) -> None:
    mission = create_mission_from_profile(safe_profile)
    mission.start(safe_profile, safety_rules)

    mission.run_to_completion()

    assert mission.state == MissionState.COMPLETED
    assert mission.status()["current_waypoint"] == "inspection"


def test_mission_without_waypoints_cannot_start(
    safe_profile: dict[str, object],
    safety_rules: dict[str, object],
) -> None:
    mission = Mission(waypoints=[])

    with pytest.raises(ValueError, match="at least one waypoint"):
        mission.start(safe_profile, safety_rules)
