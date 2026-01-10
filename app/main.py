from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.db import engine, Base
from app.websocket_manager import WebSocketManager

from app.routes.users import router as users_router
from app.routes.signals import router as signals_router, set_ws_manager as set_signals_ws
from app.routes.ws import router as ws_router, set_ws_manager as set_ws_ws

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)
    Base.metadata.create_all(bind=engine)

    ws_manager = WebSocketManager()
    set_signals_ws(ws_manager)
    set_ws_ws(ws_manager)

    app.include_router(users_router)
    app.include_router(signals_router)
    app.include_router(ws_router)
    app.mount("/web", StaticFiles(directory="web", html=True), name="web")

    @app.get("/")
    def root():
        return FileResponse("web/index.html")

    return app

app = create_app()
