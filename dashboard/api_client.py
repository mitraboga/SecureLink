import os
from typing import Any

import requests


API_BASE_URL = os.getenv("SECURELINK_API_URL", "http://api:8000")


def login(username: str, password: str, api_base_url: str = API_BASE_URL) -> str:
    response = requests.post(
        f"{api_base_url}/auth/login",
        json={"username": username, "password": password},
        timeout=10,
    )
    response.raise_for_status()
    return str(response.json()["access_token"])


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def fetch_summary(token: str, api_base_url: str = API_BASE_URL) -> dict[str, Any]:
    response = requests.get(f"{api_base_url}/security/summary", headers=auth_headers(token), timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_events(token: str, api_base_url: str = API_BASE_URL) -> list[dict[str, Any]]:
    response = requests.get(f"{api_base_url}/security/events", headers=auth_headers(token), timeout=10)
    response.raise_for_status()
    return response.json()
