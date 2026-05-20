from app.crypto.aes_service import decrypt_message, encrypt_message
from app.crypto.hash_service import sha256_hex


def test_aes_gcm_encrypts_and_decrypts_message() -> None:
    key = bytes.fromhex(sha256_hex("test-conversation"))
    encrypted = encrypt_message(key, "hello secure world")

    assert encrypted["ciphertext"] != "hello secure world"
    assert decrypt_message(key, encrypted["ciphertext"], encrypted["nonce"], encrypted["tag"]) == "hello secure world"
