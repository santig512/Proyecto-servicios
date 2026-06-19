from time import time
from typing import Dict
from starlette.requests import Request
from starlette.responses import Response

class SimpleRateLimiter:
    def __init__(self, limit: int = 100, window_seconds: int = 60):
        self.limit = limit
        self.window = window_seconds
        self.storage: Dict[str, Dict[str, float]] = {}

    def is_allowed(self, key: str) -> bool:
        now = time()
        entry = self.storage.get(key)
        if not entry:
            self.storage[key] = {"count": 1, "start": now}
            return True
        if now - entry["start"] > self.window:
            self.storage[key] = {"count": 1, "start": now}
            return True
        if entry["count"] < self.limit:
            entry["count"] += 1
            return True
        return False


def rate_limit_middleware_factory(limiter: SimpleRateLimiter):
    async def middleware(request: Request, call_next):
        client = request.client.host if request.client else "unknown"
        key = f"rl:{client}:{request.url.path}"
        if not limiter.is_allowed(key):
            return Response(status_code=429, content="Too many requests")
        response = await call_next(request)
        return response

    return middleware
