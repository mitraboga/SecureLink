import base64
import os
import uuid
from datetime import UTC, datetime
from sqlalchemy.orm import Session

from app.config import get_settings
from app.crypto.aes_service import decrypt_message, encrypt_message
from app.crypto.hmac_service import generate_hmac, verify_hmac
from app.crypto.rsa_service import sign, verify
from app.models.message import Message
from app.models.user import User
from app.services.audit_service import log_event
from app.services.detection_service import assert_not_replay
from app.services.key_session_service import get_or_create_conversation_key
from app.utils.time import utc_now_naive


def signature_payload(message_id: str, sender_id: int, receiver_id: int, ciphertext: str, nonce: str, timestamp: str) -> str:
    return "|".join([message_id, str(sender_id), str(receiver_id), ciphertext, nonce, timestamp])


def timestamp_payload(timestamp: datetime) -> str:
    if timestamp.tzinfo is not None:
        timestamp = timestamp.astimezone(UTC).replace(tzinfo=None)
    return timestamp.isoformat(timespec="microseconds")


def send_message(
    db: Session,
    sender: User,
    receiver_id: int,
    plaintext: str,
    source_ip: str | None = None,
    forced_message_id: str | None = None,
    forced_nonce: str | None = None,
) -> Message:
    receiver = db.get(User, receiver_id)
    if not receiver:
        raise ValueError("Receiver not found")

    message_id = forced_message_id or uuid.uuid4().hex
    timestamp = utc_now_naive()
    key = get_or_create_conversation_key(db, sender.id, receiver.id)
    nonce_bytes = base64.b64decode(forced_nonce) if forced_nonce else os.urandom(12)
    encrypted = encrypt_message(key, plaintext, nonce_bytes)
    assert_not_replay(db, message_id, encrypted["nonce"], timestamp, source_ip, sender.id)

    timestamp_text = timestamp_payload(timestamp)
    hmac_value = generate_hmac(key, encrypted["ciphertext"], timestamp_text, encrypted["nonce"], message_id)
    payload = signature_payload(message_id, sender.id, receiver.id, encrypted["ciphertext"], encrypted["nonce"], timestamp_text)
    signature = sign(sender.rsa_private_key_encrypted or "", get_settings().key_encryption_secret, payload)

    message = Message(
        message_id=message_id,
        sender_id=sender.id,
        receiver_id=receiver.id,
        ciphertext=encrypted["ciphertext"],
        nonce=encrypted["nonce"],
        auth_tag=encrypted["tag"],
        hmac=hmac_value,
        signature=signature,
        timestamp=timestamp,
        is_verified=True,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    log_event(db, "SECURE_MESSAGE_STORED", "INFO", f"Encrypted message {message_id} stored", source_ip, sender.id)
    return message


def decrypt_for_receiver(db: Session, message: Message, receiver: User) -> dict[str, object]:
    if message.receiver_id != receiver.id and message.sender_id != receiver.id:
        raise ValueError("Message is not visible to this user")

    key = get_or_create_conversation_key(db, message.sender_id, message.receiver_id)
    timestamp_text = timestamp_payload(message.timestamp)
    sender = db.get(User, message.sender_id)
    if not sender or not sender.rsa_public_key:
        raise ValueError("Sender public key missing")

    if not verify_hmac(key, message.hmac, message.ciphertext, timestamp_text, message.nonce, message.message_id):
        log_event(db, "HMAC_VERIFICATION_FAILED", "HIGH", f"HMAC failed for message {message.message_id}", user_id=receiver.id)
        raise ValueError("HMAC verification failed")

    payload = signature_payload(
        message.message_id,
        message.sender_id,
        message.receiver_id,
        message.ciphertext,
        message.nonce,
        timestamp_text,
    )
    if not verify(sender.rsa_public_key, payload, message.signature):
        log_event(db, "INVALID_SIGNATURE", "HIGH", f"Signature failed for message {message.message_id}", user_id=receiver.id)
        raise ValueError("Signature verification failed")

    plaintext = decrypt_message(key, message.ciphertext, message.nonce, message.auth_tag)
    return {
        "id": message.id,
        "message_id": message.message_id,
        "sender_id": message.sender_id,
        "receiver_id": message.receiver_id,
        "plaintext": plaintext,
        "timestamp": timestamp_text,
        "is_verified": True,
    }
