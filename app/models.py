import enum
import secrets
from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime, Enum, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

class SignalKind(str, enum.Enum):
    AWARE = "AWARE"            
    CONSIDERING = "CONSIDERING"  
    READY = "READY"            
    DND = "DND"         
    CLOSED = "CLOSED"          

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    display_name: Mapped[str] = mapped_column(String(80), nullable=False)
    api_key: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, default=lambda: secrets.token_hex(16))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    sent_signals = relationship("Signal", foreign_keys="Signal.sender_id", back_populates="sender")
    received_signals = relationship("Signal", foreign_keys="Signal.recipient_id", back_populates="recipient")

class Signal(Base):
    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)

    kind: Mapped[SignalKind] = mapped_column(Enum(SignalKind), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True, nullable=True)

    seen: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_signals")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_signals")




class Role(str, enum.Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"


class Organization(Base):
    __tablename__ = "orgs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

class Membership(Base):
    __tablename__ = "memberships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    org_id: Mapped[int] = mapped_column(ForeignKey("orgs.id"), index=True, nullable=False)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), index=True, nullable=True)

    role: Mapped[Role] = mapped_column(Enum(Role), index=True, nullable=False, default=Role.MEMBER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)



class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True, nullable=False)

    event_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)

    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    org_id: Mapped[int | None] = mapped_column(ForeignKey("orgs.id"), index=True, nullable=True)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), index=True, nullable=True)

    target_type: Mapped[str | None] = mapped_column(String(40), index=True, nullable=True)
    target_id: Mapped[int | None] = mapped_column(Integer, index=True, nullable=True)

    ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(240), nullable=True)

    payload_json: Mapped[str] = mapped_column(String, nullable=False, default="{}")







Index("idx_signals_recipient_created", Signal.recipient_id, Signal.created_at)
Index("idx_signals_sender_created", Signal.sender_id, Signal.created_at)
