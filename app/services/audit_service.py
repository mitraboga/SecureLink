from sqlalchemy.orm import Session

from app.models.security_event import SecurityEvent


def log_event(
    db: Session,
    event_type: str,
    severity: str,
    description: str,
    source_ip: str | None = None,
    user_id: int | None = None,
) -> SecurityEvent:
    event = SecurityEvent(
        event_type=event_type,
        severity=severity,
        description=description,
        source_ip=source_ip,
        user_id=user_id,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
