
"""CareBalance AI Alpha - API interface contract tests."""

from datetime import date, timedelta

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_forecast_response_contract():
    response = client.post(
        "/api/forecast",
        json={
            "available_staff": 9,
            "hours_per_staff": 8,
            "department": "General Care",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["department"] == "General Care"
    assert len(data["forecast"]) == 7

    for item in data["forecast"]:
        assert isinstance(item["patients"], int)
        assert isinstance(item["required_hours"], (int, float))
        assert isinstance(item["capacity_hours"], (int, float))
        assert item["required_hours"] >= 0
        assert item["capacity_hours"] >= 0
        assert item["risk"] in ("Low", "Moderate", "High")


def test_zero_staffing_nullable_utilization():
    response = client.post(
        "/api/forecast",
        json={"available_staff": 0},
    )

    assert response.status_code == 200

    for item in response.json()["forecast"]:
        assert item["capacity_hours"] == 0
        assert item["utilization_pct"] is None
        assert item["risk"] == "High"


def test_forecast_dates_are_consecutive():
    response = client.post("/api/forecast", json={})

    assert response.status_code == 200
    forecast = response.json()["forecast"]

    dates = [date.fromisoformat(item["date"]) for item in forecast]

    assert len(dates) == 7
    assert all(
        dates[i + 1] - dates[i] == timedelta(days=1)
        for i in range(6)
    )


def test_invalid_request_boundaries():
    invalid_requests = [
        {"available_staff": -1},
        {"available_staff": 1001},
        {"hours_per_staff": 0},
        {"hours_per_staff": 25},
        {"department": ""},
    ]

    for payload in invalid_requests:
        response = client.post("/api/forecast", json=payload)
        assert response.status_code == 422


def test_cors_preflight():
    response = client.options(
        "/api/forecast",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert (
        response.headers["access-control-allow-origin"]
        == "http://localhost:5173"
    )
