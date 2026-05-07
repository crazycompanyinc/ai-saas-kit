"""SQLAlchemy models for AI SaaS Kit."""

from datetime import datetime

from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, Index
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Tenant(Base):
    """A tenant (project/organization using the API)."""
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    api_key_hash = Column(String(64), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    plan = Column(String(50), default="free")  # free, pro, enterprise
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    usage_records = relationship("UsageRecord", back_populates="tenant", lazy="selectin")
    api_calls = relationship("ApiCall", back_populates="tenant", lazy="selectin")

    __table_args__ = (
        Index("ix_tenants_api_key_active", "api_key_hash", "is_active"),
    )


class UsageRecord(Base):
    """Aggregated usage per tenant per day."""
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    date = Column(String(10), nullable=False)  # YYYY-MM-DD
    total_requests = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="usage_records")

    __table_args__ = (
        Index("ix_usage_tenant_date", "tenant_id", "date", unique=True),
    )


class ApiCall(Base):
    """Individual API call log for auditing."""
    __tablename__ = "api_calls"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    response_time_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="api_calls")

    __table_args__ = (
        Index("ix_api_calls_tenant_created", "tenant_id", "created_at"),
    )


class PromptTemplate(Base):
    """Reusable prompt templates."""
    __tablename__ = "prompt_templates"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False)
    description = Column(Text, default="")
    template = Column(Text, nullable=False)
    variables = Column(Text, default="[]")  # JSON array of variable names
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_prompt_templates_tenant_slug", "tenant_id", "slug", unique=True),
    )
