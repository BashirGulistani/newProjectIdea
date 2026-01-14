import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, Tuple

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse



@dataclass
class RateLimitConfig:
    max_requests: int = 120
    window_seconds: int = 60


class SimpleRateLimitMiddleware(BaseHTTPMiddleware):
    """
    MVP-grade rate limiter:
    - Buckets by API key if present, else by client IP
    - Fixed window with rolling deque (good enough for MVP)
    - In-memory only (restart clears)
    """

    def __init__(self, app, config: RateLimitConfig | None = None):
        super().__init__(app)
        self.config = config or RateLimitConfig()
        self._hits: Dict[str, Deque[float]] = defaultdict(deque)

    def _bucket_key(self, request: Request) -> str:
        api_key = request.headers.get("x-api-key")
        if api_key:
            return f"k:{api_key}"
        ip = request.client.host if request.client else "unknown"
        return f"ip:{ip}"



    def _prune(self, dq: Deque[float], now: float) -> None:
        cutoff = now - self.config.window_seconds
        while dq and dq[0] < cutoff:
            dq.popleft()



    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path.startswith("/web") or path in ("/", "/favicon.ico"):
            return await call_next(request)









