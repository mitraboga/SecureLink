import hmac
from hashlib import sha256


def generate_hmac(secret_key: bytes, *parts: str) -> str:
    payload = "|".join(parts).encode("utf-8")
    return hmac.new(secret_key, payload, sha256).hexdigest()


def verify_hmac(secret_key: bytes, expected: str, *parts: str) -> bool:
    actual = generate_hmac(secret_key, *parts)
    return hmac.compare_digest(actual, expected)
