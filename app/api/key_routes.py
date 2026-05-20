from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_settings
from app.crypto.dh_service import derive_shared_key, generate_private_key, public_key_pem
from app.crypto.rsa_service import generate_rsa_keypair
from app.database import get_db
from app.models.user import User
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/keys", tags=["keys"])


@router.post("/generate-rsa")
def generate_rsa(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, str]:
    public_key, encrypted_private_key = generate_rsa_keypair(get_settings().key_encryption_secret)
    current_user.rsa_public_key = public_key
    current_user.rsa_private_key_encrypted = encrypted_private_key
    db.commit()
    return {"public_key": public_key}


@router.post("/exchange-dh")
def exchange_dh() -> dict[str, str]:
    alice_private = generate_private_key()
    bob_private = generate_private_key()
    alice_public = public_key_pem(alice_private)
    bob_public = public_key_pem(bob_private)
    return {
        "alice_public_key": alice_public,
        "bob_public_key": bob_public,
        "alice_shared_key": derive_shared_key(alice_private, bob_public),
        "bob_shared_key": derive_shared_key(bob_private, alice_public),
    }


@router.get("/public/{user_id}")
def public_key(user_id: int, db: Session = Depends(get_db)) -> dict[str, object]:
    user = db.get(User, user_id)
    if not user or not user.rsa_public_key:
        raise HTTPException(status_code=404, detail="Public key not found")
    return {"user_id": user.id, "username": user.username, "rsa_public_key": user.rsa_public_key}
