from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.message import Message
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.message_service import decrypt_for_receiver, send_message

router = APIRouter(prefix="/messages", tags=["messages"])


class SendMessageRequest(BaseModel):
    receiver_id: int
    plaintext: str
    message_id: str | None = None
    nonce: str | None = None


@router.post("/send", status_code=status.HTTP_201_CREATED)
def send(payload: SendMessageRequest, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, object]:
    try:
        message = send_message(
            db,
            current_user,
            payload.receiver_id,
            payload.plaintext,
            request.client.host if request.client else None,
            payload.message_id,
            payload.nonce,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": message.id,
        "message_id": message.message_id,
        "ciphertext": message.ciphertext,
        "nonce": message.nonce,
        "auth_tag": message.auth_tag,
        "hmac": message.hmac,
        "signature": message.signature,
        "timestamp": message.timestamp.isoformat(),
    }


@router.get("/inbox")
def inbox(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[dict[str, object]]:
    messages = db.query(Message).filter(Message.receiver_id == current_user.id).order_by(Message.created_at.desc()).all()
    decrypted = []
    for message in messages:
        try:
            decrypted.append(decrypt_for_receiver(db, message, current_user))
        except ValueError as exc:
            decrypted.append({"id": message.id, "message_id": message.message_id, "error": str(exc), "is_verified": False})
    return decrypted


@router.get("/{message_id}")
def get_message(message_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, object]:
    message = db.query(Message).filter(Message.message_id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    try:
        return decrypt_for_receiver(db, message, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
