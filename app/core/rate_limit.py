"""Rate limiting middleware with Redis or in-memory fallback."""

import time
from collections import defaultdict
from typing import Optional

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class InMemoryRateLimiter:
    """Simple in-memory rate limiter (fallback when Redis is unavailable)."""

    def __init__(self):
        self._requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str, max_requests: int, window: int) -> bool:
        now = time.time()
        # Clean old entries
        self._requests[key] = [
            ts for ts in self._requests[key] if now - ts < window
        ]
        if len(self._requests[key]) >= max_requests:
            return False
        self._requests[key].append(now)
        return True


_rate_limiter = InMemoryRateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware — keys on API key or IP."""

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health and static
        if request.url.path in ("/health", "/") or request.url.path.startswith("/static"):
            return await call_next(request)

        # Extract key: prefer API key, fallback to IP
        api_key = request.headers.get("X-API-Key", "")
        client_ip = request.client.host if request.client else "unknown"
        key = f"ratelimit:{api_key or client_ip}"

        if not _rate_limiter.is_allowed(
            key,
            settings.RATE_LIMIT_REQUESTS,
            settings.RATE_LIMIT_WINDOW,
        ):
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later.",
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_REQUESTS)
        response.headers["X-RateLimit-Window"] = str(settings.RATE_LIMIT_WINDOW)
        return response
