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


