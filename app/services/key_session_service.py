import base64

from cryptography.fernet import Fernet
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.crypto.dh_service import derive_shared_key, generate_private_key, public_key_pem
from app.crypto.hash_service import sha256_hex
from app.models.conversation_session import ConversationSession


def _fernet() -> Fernet:
    digest = bytes.fromhex(sha256_hex(get_settings().key_encryption_secret))[:32]
    return Fernet(base64.urlsafe_b64encode(digest))


def _pair(user_a_id: int, user_b_id: int) -> tuple[int, int]:
    return tuple(sorted([user_a_id, user_b_id]))


def get_or_create_conversation_key(db: Session, user_a_id: int, user_b_id: int) -> bytes:
    user_low_id, user_high_id = _pair(user_a_id, user_b_id)
    session = (
        db.query(ConversationSession)
        .filter(
            ConversationSession.user_low_id == user_low_id,
            ConversationSession.user_high_id == user_high_id,
        )
        .first()
    )
    if session:
        return _fernet().decrypt(session.encrypted_session_key.encode("ascii"))

    low_private = generate_private_key()
    high_private = generate_private_key()
    low_public = public_key_pem(low_private)
    high_public = public_key_pem(high_private)
    low_shared_key = base64.b64decode(derive_shared_key(low_private, high_public))
    high_shared_key = base64.b64decode(derive_shared_key(high_private, low_public))
    if low_shared_key != high_shared_key:
        raise ValueError("Diffie-Hellman key agreement failed")

    session = ConversationSession(
        user_low_id=user_low_id,
        user_high_id=user_high_id,
        user_low_dh_public_key=low_public,
        user_high_dh_public_key=high_public,
        encrypted_session_key=_fernet().encrypt(low_shared_key).decode("ascii"),
    )
    db.add(session)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return get_or_create_conversation_key(db, user_a_id, user_b_id)
    return low_shared_key
