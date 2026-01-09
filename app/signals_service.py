from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import Signal, User, utcnow

def compute_expires_at(ttl_minutes: int | None) -> datetime | None:
    if ttl_minutes is None:
        return None
    return utcnow() + timedelta(minutes=ttl_minutes)

def create_signal(db: Session, sender: User, sender_id: int, recipient_id: int, kind, ttl_minutes: int | None):
    # Sender must match auth user
    if sender.id != sender_id:
        raise PermissionError("Sender does not match authenticated user")

    recipient = db.query(User).filter(User.id == recipient_id).first()
    if not recipient:
        raise ValueError("Recipient not found")

    sig = Signal(
        sender_id=sender_id,
        recipient_id=recipient_id,
        kind=kind,
        expires_at=compute_expires_at(ttl_minutes),
    )
    db.add(sig)
    db.commit()
    db.refresh(sig)
    return sig

def list_inbox(db: Session, user_id: int, include_expired: bool = False, limit: int = 100):
    q = db.query(Signal).filter(Signal.recipient_id == user_id).order_by(Signal.created_at.desc())
    if not include_expired:
        now = datetime.now(timezone.utc)
        q = q.filter(and_(Signal.expires_at.is_(None) | (Signal.expires_at > now)))
    return q.limit(limit).all()

def list_outbox(db: Session, user_id: int, include_expired: bool = False, limit: int = 100):
    q = db.query(Signal).filter(Signal.sender_id == user_id).order_by(Signal.created_at.desc())
    if not include_expired:
        now = datetime.now(timezone.utc)
        q = q.filter(and_(Signal.expires_at.is_(None) | (Signal.expires_at > now)))
    return q.limit(limit).all()

def mark_seen(db: Session, user_id: int, signal_id: int):
    sig = db.query(Signal).filter(Signal.id == signal_id).first()
    if not sig:
        raise ValueError("Signal not found")
    if sig.recipient_id != user_id:
        raise PermissionError("Cannot mark seen: not your inbox")

    if not sig.seen:
        sig.seen = True
        sig.seen_at = utcnow()
        db.commit()
        db.refresh(sig)
    return sig
