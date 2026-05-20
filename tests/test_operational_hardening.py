from fastapi.testclient import TestClient

from app.main import app


def test_health_ready_metrics_and_security_headers() -> None:
    with TestClient(app) as client:
        health = client.get("/health")
        assert health.status_code == 200
        assert health.headers["x-content-type-options"] == "nosniff"
        assert health.headers["x-frame-options"] == "DENY"

        ready = client.get("/ready")
        assert ready.status_code == 200
        assert ready.json()["status"] == "ready"

        metrics = client.get("/metrics")
        assert metrics.status_code == 200
        assert "securelink_http_requests_total" in metrics.text


def test_rate_limit_headers_are_returned() -> None:
    with TestClient(app) as client:
        response = client.get("/auth/me")
        assert response.status_code == 401
        assert response.headers["x-ratelimit-limit"]
        assert response.headers["x-ratelimit-remaining"]
