import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


RFC3526_GROUP14_P_HEX = """
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
"""

PARAMETERS: dh.DHParameters | None = None


def parameters() -> dh.DHParameters:
    global PARAMETERS
    if PARAMETERS is None:
        p = int("".join(RFC3526_GROUP14_P_HEX.split()), 16)
        PARAMETERS = dh.DHParameterNumbers(p, 2).parameters()
    return PARAMETERS


def generate_private_key() -> dh.DHPrivateKey:
    return parameters().generate_private_key()


def public_key_pem(private_key: dh.DHPrivateKey) -> str:
    return private_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")


def derive_shared_key(private_key: dh.DHPrivateKey, peer_public_pem: str) -> str:
    peer_public_key = serialization.load_pem_public_key(peer_public_pem.encode("utf-8"))
    shared_secret = private_key.exchange(peer_public_key)
    derived = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"securelink-dh").derive(shared_secret)
    return base64.b64encode(derived).decode("ascii")
