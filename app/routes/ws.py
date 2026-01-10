from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.websocket_manager import WebSocketManager

router = APIRouter(tags=["ws"])

ws_manager: WebSocketManager | None = None

def set_ws_manager(m: WebSocketManager):
    global ws_manager
    ws_manager = m


