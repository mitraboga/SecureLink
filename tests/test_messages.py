from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def _register_and_login(client: TestClient, name: str) -> tuple[int, str]:
    response = client.post(
        "/auth/register",
        json={"username": name, "email": f"{name}@example.com", "password": "StrongPass123"},
    )
    assert response.status_code == 201
    login = client.post("/auth/login", json={"username": name, "password": "StrongPass123"})
    assert login.status_code == 200
    return response.json()["id"], login.json()["access_token"]


def test_secure_message_round_trip_and_tamper_detection() -> None:
    with TestClient(app) as client:
        suffix = uuid4().hex
        _, alice_token = _register_and_login(client, f"alice_{suffix}")
        bob_id, bob_token = _register_and_login(client, f"bob_{suffix}")

        send = client.post(
            "/messages/send",
            headers={"Authorization": f"Bearer {alice_token}"},
            json={"receiver_id": bob_id, "plaintext": "classified demo note"},
        )
        assert send.status_code == 201

        inbox = client.get("/messages/inbox", headers={"Authorization": f"Bearer {bob_token}"})
        assert inbox.status_code == 200
        assert inbox.json()[0]["plaintext"] == "classified demo note"

        tamper = client.post("/security/simulate/tamper", headers={"Authorization": f"Bearer {bob_token}"})
        assert tamper.status_code == 200
        assert tamper.json()["status"] == "blocked"

        invalid_signature = client.post(
            "/security/simulate/invalid-signature",
            headers={"Authorization": f"Bearer {bob_token}"},
        )
        assert invalid_signature.status_code == 200
        assert invalid_signature.json()["status"] == "blocked"
