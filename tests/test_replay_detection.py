from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def _register_and_login(client: TestClient, name: str) -> tuple[int, str]:
    response = client.post(
        "/auth/register",
        json={"username": name, "email": f"{name}@example.com", "password": "StrongPass123"},
    )
    assert response.status_code == 201
    user_id = response.json()["id"]
    login = client.post("/auth/login", json={"username": name, "password": "StrongPass123"})
    assert login.status_code == 200
    return user_id, login.json()["access_token"]


def test_replay_simulation_is_blocked() -> None:
    with TestClient(app) as client:
        suffix = uuid4().hex
        _, alice_token = _register_and_login(client, f"alice_{suffix}")
        bob_id, _ = _register_and_login(client, f"bob_{suffix}")

        send = client.post(
            "/messages/send",
            headers={"Authorization": f"Bearer {alice_token}"},
            json={"receiver_id": bob_id, "plaintext": "meet at 10"},
        )
        assert send.status_code == 201

        replay = client.post("/security/simulate/replay", headers={"Authorization": f"Bearer {alice_token}"})
        assert replay.status_code == 200
        assert replay.json()["status"] == "blocked"
