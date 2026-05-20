import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_message(key: bytes, plaintext: str, nonce: bytes | None = None) -> dict[str, str]:
    nonce = nonce or os.urandom(12)
    encrypted = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), None)
    ciphertext, tag = encrypted[:-16], encrypted[-16:]
    return {
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "tag": base64.b64encode(tag).decode("ascii"),
    }


def decrypt_message(key: bytes, ciphertext: str, nonce: str, tag: str) -> str:
    encrypted = base64.b64decode(ciphertext) + base64.b64decode(tag)
    plaintext = AESGCM(key).decrypt(base64.b64decode(nonce), encrypted, None)
    return plaintext.decode("utf-8")
