from fastapi.testclient import TestClient

from app.main import app


def test_diffie_hellman_exchange_returns_matching_shared_keys() -> None:
    with TestClient(app) as client:
        response = client.post("/keys/exchange-dh")
        assert response.status_code == 200
        payload = response.json()
        assert payload["alice_shared_key"] == payload["bob_shared_key"]
        assert "BEGIN PUBLIC KEY" in payload["alice_public_key"]
        assert "BEGIN PUBLIC KEY" in payload["bob_public_key"]
