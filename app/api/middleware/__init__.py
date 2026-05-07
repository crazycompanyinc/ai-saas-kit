"""API key authentication middleware."""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security import hash_api_key
from app.models import Tenant


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Validate API key on protected routes."""

    # Paths that don't require authentication
    PUBLIC_PATHS = {"/health", "/", "/docs", "/redoc", "/openapi.json", "/docs-api"}

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Check if path is public
        if any(path == p or path.startswith(p + "/") for p in self.PUBLIC_PATHS):
            return await call_next(request)

        # API routes require key (handled per-route via dependency)
        return await call_next(request)
