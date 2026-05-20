from app.crypto.rsa_service import generate_rsa_keypair, sign, verify


def test_rsa_signature_verification_rejects_modified_payload() -> None:
    public_key, encrypted_private = generate_rsa_keypair("test-secret")
    signature = sign(encrypted_private, "test-secret", "message metadata")

    assert verify(public_key, "message metadata", signature)
    assert not verify(public_key, "modified metadata", signature)
