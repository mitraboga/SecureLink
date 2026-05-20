import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.fernet import Fernet

from app.crypto.hash_service import sha256_hex


def _fernet(secret: str) -> Fernet:
    digest = bytes.fromhex(sha256_hex(secret))[:32]
    return Fernet(base64.urlsafe_b64encode(digest))


def generate_rsa_keypair(encryption_secret: str) -> tuple[str, str]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    encrypted_private = _fernet(encryption_secret).encrypt(private_pem).decode("ascii")
    return public_pem.decode("ascii"), encrypted_private


def sign(encrypted_private_key: str, encryption_secret: str, payload: str) -> str:
    private_pem = _fernet(encryption_secret).decrypt(encrypted_private_key.encode("ascii"))
    private_key = serialization.load_pem_private_key(private_pem, password=None)
    signature = private_key.sign(
        payload.encode("utf-8"),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    return base64.b64encode(signature).decode("ascii")


def verify(public_key_pem: str, payload: str, signature: str) -> bool:
    public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
    try:
        public_key.verify(
            base64.b64decode(signature),
            payload.encode("utf-8"),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False
