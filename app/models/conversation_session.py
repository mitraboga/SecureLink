from datetime import datetime

from sqlalchemy import DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import utc_now_naive


class ConversationSession(Base):
    __tablename__ = "conversation_sessions"
    __table_args__ = (UniqueConstraint("user_low_id", "user_high_id", name="uq_conversation_pair"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_low_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    user_high_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    user_low_dh_public_key: Mapped[str] = mapped_column(String, nullable=False)
    user_high_dh_public_key: Mapped[str] = mapped_column(String, nullable=False)
    encrypted_session_key: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now_naive)
