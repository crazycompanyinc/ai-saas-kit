"""Prompt template routes."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.routes.chat import _get_tenant_from_header
from app.models import PromptTemplate

router = APIRouter()


class CreatePromptRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-z0-9-]+$")
    description: str = Field(default="")
    template: str = Field(..., min_length=1)
    variables: list[str] = Field(default_factory=list)
    is_public: bool = Field(default=False)


class PromptResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    template: str
    variables: list[str]
    is_public: bool

    class Config:
        from_attributes = True


@router.post("", response_model=PromptResponse, status_code=201)
async def create_prompt(
    req: CreatePromptRequest,
    tenant=Depends(_get_tenant_from_header),
    db: AsyncSession = Depends(get_db),
):
    """Create a new prompt template."""
    import json
    prompt = PromptTemplate(
        tenant_id=tenant.id,
        name=req.name,
        slug=req.slug,
        description=req.description,
        template=req.template,
        variables=json.dumps(req.variables),
        is_public=req.is_public,
    )
    db.add(prompt)
    await db.flush()
    await db.refresh(prompt)
    return PromptResponse(
        id=prompt.id,
        name=prompt.name,
        slug=prompt.slug,
        description=prompt.description,
        template=prompt.template,
        variables=json.loads(prompt.variables),
        is_public=prompt.is_public,
    )


@router.get("", response_model=list[PromptResponse])
async def list_prompts(
    tenant=Depends(_get_tenant_from_header),
    db: AsyncSession = Depends(get_db),
):
    """List prompt templates for the tenant."""
    import json
    from sqlalchemy import select

    result = await db.execute(
        select(PromptTemplate).where(
            (PromptTemplate.tenant_id == tenant.id) | (PromptTemplate.is_public == True)
        )
    )
    prompts = result.scalars().all()
    return [
        PromptResponse(
            id=p.id,
            name=p.name,
            slug=p.slug,
            description=p.description,
            template=p.template,
            variables=json.loads(p.variables),
            is_public=p.is_public,
        )
        for p in prompts
    ]
