from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from robot_mock.app import api as api_module
from robot_mock.app.api import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_mission() -> None:
    api_module._mission = api_module.create_mission_from_profile(api_module._profile)


def test_health_endpoint_returns_expected_fields() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert {
        "service_status",
        "emergency_stop_state",
        "battery_percentage",
        "mission_state",
    }.issubset(payload)
    assert payload["service_status"] == "OK"
    assert payload["emergency_stop_state"] == "enabled"
    assert payload["battery_percentage"] == 87
    assert payload["mission_state"] == "IDLE"


def test_mission_endpoint_returns_profile_waypoints() -> None:
    response = client.get("/mission")

    assert response.status_code == 200
    payload = response.json()
    assert payload["state"] == "IDLE"
    assert payload["waypoints"] == ["dock", "inspection-point", "return"]
    assert payload["current_waypoint"] is None
    assert payload["failure_reason"] is None


def test_start_mission_endpoint_returns_running_state() -> None:
    response = client.post("/mission/start")

    assert response.status_code == 200
    payload = response.json()
    assert payload["state"] == "RUNNING"
    assert payload["waypoints"] == ["dock", "inspection-point", "return"]
    assert payload["current_waypoint"] is None
    assert payload["failure_reason"] is None
