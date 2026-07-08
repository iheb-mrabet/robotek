from __future__ import annotations

import pytest

from robot_mock.app.safety import (
    SafetyValidationError,
    assert_safe_robot_profile,
    validate_robot_profile,
)


@pytest.fixture
def safe_profile() -> dict[str, object]:
    return {
        "robot_name": "mock-rover-01",
        "environment": "staging",
        "max_speed_mps": 1.2,
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


def test_valid_config_passes(
    safe_profile: dict[str, object],
    safety_rules: dict[str, object],
) -> None:
    result = validate_robot_profile(safe_profile, safety_rules)

    assert result.valid is True
    assert result.messages == []


def test_disabled_emergency_stop_fails(
    safe_profile: dict[str, object],
    safety_rules: dict[str, object],
) -> None:
    unsafe_profile = safe_profile | {"emergency_stop_enabled": False}

    with pytest.raises(SafetyValidationError, match="Emergency stop"):
        assert_safe_robot_profile(unsafe_profile, safety_rules)


def test_speed_above_limit_fails(
    safe_profile: dict[str, object],
    safety_rules: dict[str, object],
) -> None:
    unsafe_profile = safe_profile | {"max_speed_mps": 2.0}

    with pytest.raises(SafetyValidationError, match="exceeds allowed limit"):
        assert_safe_robot_profile(unsafe_profile, safety_rules)


def test_debug_true_in_staging_fails(
    safe_profile: dict[str, object],
    safety_rules: dict[str, object],
) -> None:
    unsafe_profile = safe_profile | {"debug": True}

    with pytest.raises(SafetyValidationError, match="Debug mode"):
        assert_safe_robot_profile(unsafe_profile, safety_rules)
