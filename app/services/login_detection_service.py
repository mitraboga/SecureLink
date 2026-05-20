from datetime import timedelta

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.security_event import SecurityEvent
from app.services.audit_service import log_event
from app.utils.time import utc_now_naive


def track_failed_login(db: Session, username: str, source_ip: str | None) -> None:
    settings = get_settings()
    log_event(db, "LOGIN_FAILURE", "MEDIUM", f"Failed login for {username}", source_ip)

    window_start = utc_now_naive() - timedelta(seconds=settings.login_failure_window_seconds)
    recent_failures = (
        db.query(SecurityEvent)
        .filter(
            SecurityEvent.event_type == "LOGIN_FAILURE",
            SecurityEvent.source_ip == source_ip,
            SecurityEvent.created_at >= window_start,
        )
        .count()
    )
    if recent_failures >= settings.login_failure_threshold:
        already_logged = (
            db.query(SecurityEvent)
            .filter(
                SecurityEvent.event_type == "BRUTE_FORCE_LOGIN_DETECTED",
                SecurityEvent.source_ip == source_ip,
                SecurityEvent.created_at >= window_start,
            )
            .first()
        )
        if not already_logged:
            log_event(
                db,
                "BRUTE_FORCE_LOGIN_DETECTED",
                "HIGH",
                f"{recent_failures} failed logins detected within threshold window",
                source_ip,
            )
