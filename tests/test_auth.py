from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_register_login_and_me() -> None:
    with TestClient(app) as client:
        suffix = uuid4().hex
        username = f"alice_{suffix}"

        register = client.post(
            "/auth/register",
            json={"username": username, "email": f"{username}@example.com", "password": "StrongPass123"},
        )
        assert register.status_code == 201

        login = client.post("/auth/login", json={"username": username, "password": "StrongPass123"})
        assert login.status_code == 200

        token = login.json()["access_token"]
        me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me.status_code == 200
        assert me.json()["username"] == username
