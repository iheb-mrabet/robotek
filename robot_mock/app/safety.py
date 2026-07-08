"""Safety validation for mock robot configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).resolve().parents[1] / "configs"
DEFAULT_PROFILE_PATH = CONFIG_DIR / "robot_profile.yaml"
DEFAULT_RULES_PATH = CONFIG_DIR / "safety_rules.yaml"

REQUIRED_PROFILE_FIELDS = {
    "robot_name",
    "environment",
    "max_speed_mps",
    "debug",
    "emergency_stop_enabled",
    "default_mission_waypoints",
}


class SafetyValidationError(ValueError):
    """Raised when a robot profile violates safety rules."""


@dataclass(frozen=True)
class SafetyValidationResult:
    """Result of validating a robot profile against safety rules."""

    valid: bool
    messages: list[str]
    profile: dict[str, Any]
    rules: dict[str, Any]


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML file and return a dictionary."""

    config_path = Path(path)
    try:
        with config_path.open("r", encoding="utf-8") as file:
            loaded = yaml.safe_load(file)
    except FileNotFoundError as exc:
        msg = f"Configuration file not found: {config_path}"
        raise SafetyValidationError(msg) from exc
    except yaml.YAMLError as exc:
        msg = f"Invalid YAML in {config_path}: {exc}"
        raise SafetyValidationError(msg) from exc

    if not isinstance(loaded, dict):
        msg = f"Configuration file must contain a YAML mapping: {config_path}"
        raise SafetyValidationError(msg)

    return loaded


def validate_robot_profile(
    profile: dict[str, Any],
    rules: dict[str, Any],
) -> SafetyValidationResult:
    """Validate a robot profile against safety rules."""

    messages: list[str] = []
    missing_fields = sorted(REQUIRED_PROFILE_FIELDS - profile.keys())
    if missing_fields:
        messages.append(f"Missing required profile fields: {', '.join(missing_fields)}")

    max_allowed_speed = rules.get("max_allowed_speed_mps")
    require_emergency_stop = bool(rules.get("require_emergency_stop", True))
    forbid_debug_in = set(rules.get("forbid_debug_in", []))

    if require_emergency_stop and profile.get("emergency_stop_enabled") is False:
        messages.append("Emergency stop must be enabled")

    environment = profile.get("environment")
    if profile.get("debug") is True and environment in forbid_debug_in:
        messages.append(f"Debug mode is not allowed in {environment}")

    max_speed = profile.get("max_speed_mps")
    if max_speed is not None and max_allowed_speed is not None:
        try:
            if float(max_speed) > float(max_allowed_speed):
                messages.append(
                    f"Max speed {max_speed} m/s exceeds allowed limit {max_allowed_speed} m/s"
                )
        except (TypeError, ValueError):
            messages.append("Max speed and allowed speed must be numeric")

    waypoints = profile.get("default_mission_waypoints")
    if waypoints is not None:
        if not isinstance(waypoints, list) or not waypoints:
            messages.append("Default mission waypoints must be a non-empty list")

    return SafetyValidationResult(
        valid=not messages,
        messages=messages,
        profile=profile,
        rules=rules,
    )


def assert_safe_robot_profile(
    profile: dict[str, Any],
    rules: dict[str, Any],
) -> SafetyValidationResult:
    """Validate a robot profile and raise a clear exception when unsafe."""

    result = validate_robot_profile(profile, rules)
    if not result.valid:
        raise SafetyValidationError("; ".join(result.messages))
    return result


def load_default_profile() -> dict[str, Any]:
    """Load the default robot profile."""

    return load_yaml_config(DEFAULT_PROFILE_PATH)


def load_default_rules() -> dict[str, Any]:
    """Load the default safety rules."""

    return load_yaml_config(DEFAULT_RULES_PATH)
