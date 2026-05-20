import argparse

import requests


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SecureLink brute-force login simulation.")
    parser.add_argument("--api", default="http://localhost:8000")
    parser.add_argument("--username", required=True)
    args = parser.parse_args()

    for attempt in range(1, 6):
        response = requests.post(
            f"{args.api}/auth/login",
            json={"username": args.username, "password": f"wrong-password-{attempt}"},
            timeout=10,
        )
        print(attempt, response.status_code, response.json())


if __name__ == "__main__":
    main()
