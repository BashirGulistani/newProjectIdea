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










Index("idx_signals_recipient_created", Signal.recipient_id, Signal.created_at)
Index("idx_signals_sender_created", Signal.sender_id, Signal.created_at)
