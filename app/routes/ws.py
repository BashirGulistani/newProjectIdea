from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.websocket_manager import WebSocketManager

router = APIRouter(tags=["ws"])

ws_manager: WebSocketManager | None = None

def set_ws_manager(m: WebSocketManager):
    global ws_manager
    ws_manager = m




@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket, user_id: int = Query(...)):
    if ws_manager is None:
        await ws.close(code=1011)
        return

    await ws_manager.connect(user_id, ws)
    try:
        while True:
            msg = await ws.receive_text()
            if msg.strip().lower() == "ping":
                await ws.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id, ws)
    except Exception:
        ws_manager.disconnect(user_id, ws)
        try:
            await ws.close(code=1011)
        except Exception:
            pass
