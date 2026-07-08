"""Minimal FastAPI app for the mock robot."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from robot_mock.app.health import get_robot_health
from robot_mock.app.mission import Mission, create_mission_from_profile
from robot_mock.app.safety import (
    SafetyValidationError,
    load_default_profile,
    load_default_rules,
)

app = FastAPI(title="Robot DevSecOps Mock API", version="0.1.0")

_profile = load_default_profile()
_rules = load_default_rules()
_mission: Mission = create_mission_from_profile(_profile)


@app.get("/health")
def health() -> dict[str, object]:
    """Return mock robot health."""

    return get_robot_health(mission_state=_mission.state, profile=_profile)


@app.get("/mission")
def mission_status() -> dict[str, object]:
    """Return current mission state."""

    return _mission.status()


@app.post("/mission/start")
def start_mission() -> dict[str, object]:
    """Start the configured mock mission."""

    global _mission
    _mission = create_mission_from_profile(_profile)

    try:
        _mission.start(_profile, _rules)
    except SafetyValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return _mission.status()
