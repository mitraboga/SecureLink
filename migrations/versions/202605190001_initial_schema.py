"""initial schema

Revision ID: 202605190001
Revises:
Create Date: 2026-05-19
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "202605190001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("rsa_public_key", sa.String(), nullable=True),
        sa.Column("rsa_private_key_encrypted", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "conversation_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_low_id", sa.Integer(), nullable=False),
        sa.Column("user_high_id", sa.Integer(), nullable=False),
        sa.Column("user_low_dh_public_key", sa.String(), nullable=False),
        sa.Column("user_high_dh_public_key", sa.String(), nullable=False),
        sa.Column("encrypted_session_key", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_low_id", "user_high_id", name="uq_conversation_pair"),
    )
    op.create_index(op.f("ix_conversation_sessions_id"), "conversation_sessions", ["id"], unique=False)
    op.create_index(op.f("ix_conversation_sessions_user_low_id"), "conversation_sessions", ["user_low_id"], unique=False)
    op.create_index(op.f("ix_conversation_sessions_user_high_id"), "conversation_sessions", ["user_high_id"], unique=False)

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("message_id", sa.String(length=64), nullable=False),
        sa.Column("sender_id", sa.Integer(), nullable=False),
        sa.Column("receiver_id", sa.Integer(), nullable=False),
        sa.Column("ciphertext", sa.Text(), nullable=False),
        sa.Column("nonce", sa.String(length=64), nullable=False),
        sa.Column("auth_tag", sa.String(length=64), nullable=False),
        sa.Column("hmac", sa.String(length=128), nullable=False),
        sa.Column("signature", sa.Text(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["receiver_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["sender_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_messages_id"), "messages", ["id"], unique=False)
    op.create_index(op.f("ix_messages_message_id"), "messages", ["message_id"], unique=True)
    op.create_index(op.f("ix_messages_nonce"), "messages", ["nonce"], unique=True)

    op.create_table(
        "security_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("source_ip", sa.String(length=80), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_security_events_id"), "security_events", ["id"], unique=False)
    op.create_index(op.f("ix_security_events_event_type"), "security_events", ["event_type"], unique=False)
    op.create_index(op.f("ix_security_events_severity"), "security_events", ["severity"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_security_events_severity"), table_name="security_events")
    op.drop_index(op.f("ix_security_events_event_type"), table_name="security_events")
    op.drop_index(op.f("ix_security_events_id"), table_name="security_events")
    op.drop_table("security_events")
    op.drop_index(op.f("ix_messages_nonce"), table_name="messages")
    op.drop_index(op.f("ix_messages_message_id"), table_name="messages")
    op.drop_index(op.f("ix_messages_id"), table_name="messages")
    op.drop_table("messages")
    op.drop_index(op.f("ix_conversation_sessions_user_high_id"), table_name="conversation_sessions")
    op.drop_index(op.f("ix_conversation_sessions_user_low_id"), table_name="conversation_sessions")
    op.drop_index(op.f("ix_conversation_sessions_id"), table_name="conversation_sessions")
    op.drop_table("conversation_sessions")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
