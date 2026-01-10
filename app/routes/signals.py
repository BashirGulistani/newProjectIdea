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


