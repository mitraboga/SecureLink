from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.message import Message
from app.models.security_event import SecurityEvent
from app.models.user import User
from app.services.audit_service import log_event
from app.services.auth_service import get_current_user
from app.services.message_service import decrypt_for_receiver, send_message

router = APIRouter(prefix="/security", tags=["security"])


@router.get("/events")
def events(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[dict[str, object]]:
    rows = db.query(SecurityEvent).order_by(SecurityEvent.created_at.desc()).limit(100).all()
    return [
        {
            "id": row.id,
            "event_type": row.event_type,
            "severity": row.severity,
            "source_ip": row.source_ip,
            "user_id": row.user_id,
            "description": row.description,
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]


@router.get("/summary")
def summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, object]:
    grouped = db.query(SecurityEvent.event_type, func.count(SecurityEvent.id)).group_by(SecurityEvent.event_type).all()
    severity = db.query(SecurityEvent.severity, func.count(SecurityEvent.id)).group_by(SecurityEvent.severity).all()
    return {
        "total_events": db.query(SecurityEvent).count(),
        "by_event_type": {name: count for name, count in grouped},
        "by_severity": {name: count for name, count in severity},
    }


@router.post("/simulate/replay")
def simulate_replay(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, str]:
    latest = db.query(Message).filter(Message.sender_id == current_user.id).order_by(Message.created_at.desc()).first()
    if not latest:
        raise HTTPException(status_code=400, detail="Send a message before simulating replay")
    try:
        send_message(
            db,
            current_user,
            latest.receiver_id,
            "replayed payload",
            request.client.host if request.client else None,
            forced_message_id=latest.message_id,
            forced_nonce=latest.nonce,
        )
    except ValueError as exc:
        return {"status": "blocked", "reason": str(exc)}
    return {"status": "unexpectedly accepted"}


@router.post("/simulate/tamper")
def simulate_tamper(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, str]:
    latest = db.query(Message).filter(Message.receiver_id == current_user.id).order_by(Message.created_at.desc()).first()
    if not latest:
        raise HTTPException(status_code=400, detail="Receive a message before simulating tampering")
    original = latest.ciphertext
    latest.ciphertext = ("B" if latest.ciphertext.startswith("A") else "A") + latest.ciphertext[1:]
    db.commit()
    try:
        decrypt_for_receiver(db, latest, current_user)
    except ValueError as exc:
        latest.ciphertext = original
        db.commit()
        return {"status": "blocked", "reason": str(exc)}
    latest.ciphertext = original
    db.commit()
    log_event(db, "MESSAGE_TAMPERING_ATTEMPT", "HIGH", f"Tamper simulation for {latest.message_id}", user_id=current_user.id)
    return {"status": "unexpectedly accepted"}


@router.post("/simulate/invalid-signature")
def simulate_invalid_signature(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, str]:
    latest = db.query(Message).filter(Message.receiver_id == current_user.id).order_by(Message.created_at.desc()).first()
    if not latest:
        raise HTTPException(status_code=400, detail="Receive a message before simulating invalid signature")
    original = latest.signature
    latest.signature = ("B" if latest.signature.startswith("A") else "A") + latest.signature[1:]
    db.commit()
    try:
        decrypt_for_receiver(db, latest, current_user)
    except ValueError as exc:
        latest.signature = original
        db.commit()
        return {"status": "blocked", "reason": str(exc)}
    latest.signature = original
    db.commit()
    return {"status": "unexpectedly accepted"}


@router.post("/simulate/mitm")
def simulate_mitm(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, str]:
    log_event(db, "MITM_SIMULATION_BLOCKED", "MEDIUM", "MITM demo blocked because signature/HMAC keys do not match", user_id=current_user.id)
    return {"status": "blocked", "reason": "A forged sender cannot produce the valid HMAC and RSA signature"}
