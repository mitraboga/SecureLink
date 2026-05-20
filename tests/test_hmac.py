from app.crypto.hash_service import sha256_hex
from app.crypto.hmac_service import generate_hmac, verify_hmac


def test_hmac_rejects_tampered_payload() -> None:
    key = bytes.fromhex(sha256_hex("hmac-key"))
    digest = generate_hmac(key, "ciphertext", "timestamp", "nonce")

    assert verify_hmac(key, digest, "ciphertext", "timestamp", "nonce")
    assert not verify_hmac(key, digest, "tampered", "timestamp", "nonce")
