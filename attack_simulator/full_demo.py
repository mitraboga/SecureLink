import argparse
from uuid import uuid4

import requests


def post(api: str, path: str, token: str | None = None, **json):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.post(f"{api}{path}", headers=headers, json=json or None, timeout=30)
    response.raise_for_status()
    return response.json()


def get(api: str, path: str, token: str):
    response = requests.get(f"{api}{path}", headers={"Authorization": f"Bearer {token}"}, timeout=30)
    response.raise_for_status()
    return response.json()


def register_and_login(api: str, username: str) -> tuple[int, str]:
    post(api, "/auth/register", username=username, email=f"{username}@example.com", password="StrongPass123")
    login = post(api, "/auth/login", username=username, password="StrongPass123")
    user = get(api, "/auth/me", login["access_token"])
    return int(user["id"]), login["access_token"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the complete SecureLink demo workflow.")
    parser.add_argument("--api", default="http://localhost:8000")
    args = parser.parse_args()

    suffix = uuid4().hex[:8]
    alice_id, alice_token = register_and_login(args.api, f"alice_{suffix}")
    bob_id, bob_token = register_and_login(args.api, f"bob_{suffix}")

    message = post(
        args.api,
        "/messages/send",
        alice_token,
        receiver_id=bob_id,
        plaintext="SecureLink demo message: AES-GCM, HMAC, and RSA signatures are active.",
    )
    inbox = get(args.api, "/messages/inbox", bob_token)
    replay = post(args.api, "/security/simulate/replay", alice_token)
    tamper = post(args.api, "/security/simulate/tamper", bob_token)
    invalid_signature = post(args.api, "/security/simulate/invalid-signature", bob_token)
    mitm = post(args.api, "/security/simulate/mitm", alice_token)
    summary = get(args.api, "/security/summary", alice_token)

    print(
        {
            "alice_id": alice_id,
            "bob_id": bob_id,
            "message_id": message["message_id"],
            "bob_inbox_first_message": inbox[0],
            "replay": replay,
            "tamper": tamper,
            "invalid_signature": invalid_signature,
            "mitm": mitm,
            "security_summary": summary,
        }
    )


if __name__ == "__main__":
    main()
