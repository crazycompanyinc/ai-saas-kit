"""API route aggregation."""

from app.api.routes import tenants, chat, usage, prompts

api_router = None

from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(usage.router, prefix="/usage", tags=["usage"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
