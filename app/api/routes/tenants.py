"""Tenant management routes."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.tenant_service import tenant_service

router = APIRouter()


class CreateTenantRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-z0-9-]+$")


class TenantResponse(BaseModel):
    id: int
    name: str
    slug: str
    plan: str
    is_active: bool
    api_key: str | None = None  # Only shown on creation


class TenantListResponse(BaseModel):
    id: int
    name: str
    slug: str
    plan: str
    is_active: bool


@router.post("", response_model=TenantResponse, status_code=201)
async def create_tenant(
    req: CreateTenantRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a new tenant. Returns the tenant with API key (shown once)."""
    tenant, api_key = await tenant_service.create_tenant(db, req.name, req.slug)
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        slug=tenant.slug,
        plan=tenant.plan,
        is_active=tenant.is_active,
        api_key=api_key,
    )


@router.post("/{tenant_id}/regenerate-key", response_model=TenantResponse)
async def regenerate_key(tenant_id: int, db: AsyncSession = Depends(get_db)):
    """Regenerate API key for a tenant."""
    tenant, api_key = await tenant_service.regenerate_api_key(db, tenant_id)
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        slug=tenant.slug,
        plan=tenant.plan,
        is_active=tenant.is_active,
        api_key=api_key,
    )
