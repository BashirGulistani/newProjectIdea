from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth import require_api_key, require_user_or_403
from app.schemas import SignalCreate, SignalOut, MarkSeenOut
from app.signals_service import create_signal, list_inbox, list_outbox, mark_seen
from app.websocket_manager import WebSocketManager

router = APIRouter(prefix="/signals", tags=["signals"])

ws_manager: WebSocketManager | None = None

def set_ws_manager(m: WebSocketManager):
    global ws_manager
    ws_manager = m


@router.post("", response_model=SignalOut)
async def send_signal(payload: SignalCreate, db: Session = Depends(get_db), auth_user=Depends(require_api_key)):
    try:
        sig = create_signal(
            db=db,
            sender=auth_user,
            sender_id=payload.sender_id,
            recipient_id=payload.recipient_id,
            kind=payload.kind,
            ttl_minutes=payload.ttl_minutes,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if ws_manager:
        await ws_manager.push_to_user(sig.recipient_id, {
            "type": "signal_created",
            "signal": {
                "id": sig.id,
                "sender_id": sig.sender_id,
                "recipient_id": sig.recipient_id,
                "kind": sig.kind,
                "created_at": sig.created_at.isoformat(),
                "expires_at": sig.expires_at.isoformat() if sig.expires_at else None,
                "seen": sig.seen,
                "seen_at": sig.seen_at.isoformat() if sig.seen_at else None,
            }
        })

    return sig



@router.get("/inbox", response_model=list[SignalOut])
def inbox(
    user_id: int = Query(...),
    include_expired: bool = Query(False),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    auth_user=Depends(require_api_key),
):
    require_user_or_403(user_id=user_id, auth_user=auth_user)
    return list_inbox(db, user_id=user_id, include_expired=include_expired, limit=limit)











