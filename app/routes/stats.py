from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.auth import require_api_key, require_user_or_403
from app.models import Signal, SignalKind, User

router = APIRouter(prefix="/stats", tags=["stats"])



@router.get("/inbox")
def inbox_stats(
    user_id: int = Query(...),
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    auth_user: User = Depends(require_api_key),
):
    """
    Simple analytics:
    - total received (last N days)
    - unseen count
    - breakdown by kind
    """
    require_user_or_403(user_id=user_id, auth_user=auth_user)

    now = datetime.now(timezone.utc)
    since = now - timedelta(days=days)

    total = (
        db.query(func.count(Signal.id))
        .filter(Signal.recipient_id == user_id, Signal.created_at >= since)
        .scalar()
        or 0
    )


    unseen = (
        db.query(func.count(Signal.id))
        .filter(Signal.recipient_id == user_id, Signal.created_at >= since, Signal.seen == False)  # noqa: E712
        .scalar()
        or 0
    )


    by_kind_rows = (
        db.query(Signal.kind, func.count(Signal.id))
        .filter(Signal.recipient_id == user_id, Signal.created_at >= since)
        .group_by(Signal.kind)
        .all()
    )

    by_kind = {str(k): int(c) for (k, c) in by_kind_rows}

    # Ensure all kinds exist in response (nice for dashboards)
    for k in SignalKind:
        by_kind.setdefault(k.value, 0)

    return {
        "user_id": user_id,
        "window_days": days,
        "total_received": int(total),
        "unseen": int(unseen),
        "by_kind": by_kind,
    }


@router.get("/outbox")
def outbox_stats(
    user_id: int = Query(...),
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    auth_user: User = Depends(require_api_key),
):
    """
    Outbox analytics:
    - total sent (last N days)
    - breakdown by kind
    - top recipients
    """


    require_user_or_403(user_id=user_id, auth_user=auth_user)

    now = datetime.now(timezone.utc)
    since = now - timedelta(days=days)

    total = (
        db.query(func.count(Signal.id))
        .filter(Signal.sender_id == user_id, Signal.created_at >= since)
        .scalar()
        or 0
    )

    by_kind_rows = (
        db.query(Signal.kind, func.count(Signal.id))
        .filter(Signal.sender_id == user_id, Signal.created_at >= since)
        .group_by(Signal.kind)
        .all()
    )
    by_kind = {str(k): int(c) for (k, c) in by_kind_rows}
    for k in SignalKind:
        by_kind.setdefault(k.value, 0)


