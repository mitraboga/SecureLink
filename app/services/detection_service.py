from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.message import Message
from app.services.audit_service import log_event
from app.utils.time import utc_now


def assert_not_replay(
    db: Session,
    message_id: str,
    nonce: str,
    timestamp: datetime,
    source_ip: str | None,
    user_id: int,
) -> None:
    settings = get_settings()
    now = utc_now()
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=UTC)

    if abs((now - timestamp).total_seconds()) > settings.replay_window_seconds:
        log_event(db, "REPLAY_ATTACK_DETECTED", "HIGH", "Rejected message with stale timestamp", source_ip, user_id)
        raise ValueError("Message timestamp is outside replay window")

    duplicate = db.query(Message).filter((Message.message_id == message_id) | (Message.nonce == nonce)).first()
    if duplicate:
        log_event(db, "REPLAY_ATTACK_DETECTED", "HIGH", "Rejected duplicate message id or nonce", source_ip, user_id)
        raise ValueError("Duplicate message id or nonce detected")
