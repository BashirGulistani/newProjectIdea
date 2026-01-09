from typing import Dict, Set
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self._connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, user_id: int, ws: WebSocket):
        await ws.accept()
        self._connections.setdefault(user_id, set()).add(ws)

    def disconnect(self, user_id: int, ws: WebSocket):
        conns = self._connections.get(user_id)
        if not conns:
            return
        conns.discard(ws)
        if not conns:
            self._connections.pop(user_id, None)

    async def push_to_user(self, user_id: int, payload: dict):
        conns = self._connections.get(user_id, set())
        dead = []
        for ws in conns:
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(user_id, ws)
