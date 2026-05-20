import argparse

import requests


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SecureLink MITM simulation.")
    parser.add_argument("--api", default="http://localhost:8000")
    parser.add_argument("--token", required=True)
    args = parser.parse_args()

    response = requests.post(
        f"{args.api}/security/simulate/mitm",
        headers={"Authorization": f"Bearer {args.token}"},
        timeout=10,
    )
    print(response.status_code, response.json())


if __name__ == "__main__":
    main()
