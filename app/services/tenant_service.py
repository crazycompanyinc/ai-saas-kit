"""Tenant management service."""

from datetime import datetime, date
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import generate_api_key, hash_api_key
from app.models import Tenant, UsageRecord, ApiCall


class TenantService:
    """Manage tenants, API keys, and usage tracking."""

    @staticmethod
    async def create_tenant(db: AsyncSession, name: str, slug: str) -> tuple[Tenant, str]:
        """Create a new tenant. Returns (tenant, raw_api_key)."""
        api_key = generate_api_key()
        tenant = Tenant(
            name=name,
            slug=slug,
            api_key_hash=hash_api_key(api_key),
        )
        db.add(tenant)
        await db.flush()
        return tenant, api_key

    @staticmethod
    async def get_by_api_key(db: AsyncSession, api_key: str) -> Optional[Tenant]:
        """Look up a tenant by API key."""
        key_hash = hash_api_key(api_key)
        result = await db.execute(
            select(Tenant).where(
                Tenant.api_key_hash == key_hash,
                Tenant.is_active == True,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def regenerate_api_key(db: AsyncSession, tenant_id: int) -> tuple[Tenant, str]:
        """Regenerate API key for a tenant."""
        result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
        tenant = result.scalar_one()
        new_key = generate_api_key()
        tenant.api_key_hash = hash_api_key(new_key)
        await db.flush()
        return tenant, new_key

    @staticmethod
    async def get_usage_summary(
        db: AsyncSession, tenant_id: int, days: int = 30
    ) -> dict:
        """Get usage summary for a tenant."""
        today = date.today()
        start_date = today.replace(day=1)  # Current month

        result = await db.execute(
            select(
                func.coalesce(func.sum(UsageRecord.total_requests), 0),
                func.coalesce(func.sum(UsageRecord.total_tokens), 0),
                func.coalesce(func.sum(UsageRecord.total_cost), 0.0),
            )
            .where(
                UsageRecord.tenant_id == tenant_id,
                UsageRecord.date >= start_date.isoformat(),
            )
        )
        row = result.one()

        # Daily breakdown
        daily_result = await db.execute(
            select(UsageRecord)
            .where(
                UsageRecord.tenant_id == tenant_id,
                UsageRecord.date >= start_date.isoformat(),
            )
            .order_by(UsageRecord.date)
        )
        daily = daily_result.scalars().all()

        return {
            "period": f"{start_date.isoformat()} to {today.isoformat()}",
            "total_requests": row[0],
            "total_tokens": row[1],
            "total_cost": round(row[2], 4),
            "daily": [
                {
                    "date": d.date,
                    "requests": d.total_requests,
                    "tokens": d.total_tokens,
                    "cost": round(d.total_cost, 4),
                }
                for d in daily
            ],
        }

    @staticmethod
    async def record_api_call(
        db: AsyncSession,
        tenant_id: int,
        endpoint: str,
        method: str,
        status_code: int,
        tokens_used: int = 0,
        cost: float = 0.0,
        response_time_ms: float = 0.0,
    ) -> None:
        """Record an API call and update daily usage."""
        # Log the call
        call = ApiCall(
            tenant_id=tenant_id,
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            tokens_used=tokens_used,
            cost=cost,
            response_time_ms=response_time_ms,
        )
        db.add(call)

        # Update daily usage
        today = date.today().isoformat()
        result = await db.execute(
            select(UsageRecord).where(
                UsageRecord.tenant_id == tenant_id,
                UsageRecord.date == today,
            )
        )
        record = result.scalar_one_or_none()

        if record:
            record.total_requests += 1
            record.total_tokens += tokens_used
            record.total_cost += cost
        else:
            record = UsageRecord(
                tenant_id=tenant_id,
                date=today,
                total_requests=1,
                total_tokens=tokens_used,
                total_cost=cost,
            )
            db.add(record)


tenant_service = TenantService()
