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





