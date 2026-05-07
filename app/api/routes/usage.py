"""Usage and analytics routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.routes.chat import _get_tenant_from_header
from app.services.tenant_service import tenant_service

router = APIRouter()


class UsageSummaryResponse(BaseModel):
    period: str
    total_requests: int
    total_tokens: int
    total_cost: float
    daily: list[dict]


# Need to import here to avoid circular
from pydantic import BaseModel as BM


class UsageSummaryResponse(BM):
    period: str
    total_requests: int
    total_tokens: int
    total_cost: float
    daily: list[dict]


@router.get("/summary", response_model=UsageSummaryResponse)
async def usage_summary(
    days: int = Query(default=30, ge=1, le=365),
    tenant=Depends(_get_tenant_from_header),
    db: AsyncSession = Depends(get_db),
):
    """Get usage summary for the current tenant."""
    summary = await tenant_service.get_usage_summary(db, tenant.id, days)
    return UsageSummaryResponse(**summary)
