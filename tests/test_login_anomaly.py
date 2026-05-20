from fastapi.testclient import TestClient

from app.main import app


def test_repeated_failed_logins_create_brute_force_event() -> None:
    with TestClient(app) as client:
        for _ in range(5):
            response = client.post("/auth/login", json={"username": "missing", "password": "wrong"})
            assert response.status_code == 401

        client.post(
            "/auth/register",
            json={"username": "admin_user", "email": "admin@example.com", "password": "StrongPass123"},
        )
        login = client.post("/auth/login", json={"username": "admin_user", "password": "StrongPass123"})
        token = login.json()["access_token"]
        events = client.get("/security/events", headers={"Authorization": f"Bearer {token}"})

        event_types = {event["event_type"] for event in events.json()}
        assert "BRUTE_FORCE_LOGIN_DETECTED" in event_types
