import asyncio
from datetime import datetime, timezone

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Signal





class CleanupService:
    """
    Background cleanup:
    - Deletes expired signals every N seconds
    - Keeps DB small and inbox queries fast
    """

    def __init__(self, interval_seconds: int = 60):
        self.interval_seconds = interval_seconds
        self._task: asyncio.Task | None = None
        self._stop = asyncio.Event()

    def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._run())


    async def stop(self) -> None:
        self._stop.set()
        if self._task:
            await self._task
            self._task = None
        self._stop.clear()



