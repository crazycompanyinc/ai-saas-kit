"""AI Chat routes — proxy to OpenAI/Anthropic with usage tracking."""

from fastapi import APIRouter, Depends, HTTPException, Header, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.ai_service import ai_service
from app.services.tenant_service import tenant_service

router = APIRouter()


class ChatMessage(BaseModel):
    role: str = Field(..., pattern=r"^(system|user|assistant)$")
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., min_length=1)
    model: str = Field(default="gpt-4o-mini")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1, le=8192)
    stream: bool = Field(default=False)


class ChatResponse(BaseModel):
    content: str
    model: str
    provider: str
    tokens: dict
    response_time_ms: float


def _cost_for_model(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculate estimated cost per 1K tokens."""
    pricing = {
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "claude-sonnet-4-20250514": {"input": 0.003, "output": 0.015},
        "claude-3-5-haiku-20241022": {"input": 0.0008, "output": 0.004},
    }
    rates = pricing.get(model, {"input": 0.001, "output": 0.002})
    return (prompt_tokens / 1000 * rates["input"]) + (completion_tokens / 1000 * rates["output"])


async def _get_tenant_from_header(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: AsyncSession = Depends(get_db),
):
    """Dependency: resolve tenant from API key."""
    tenant = await tenant_service.get_by_api_key(db, x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")
    return tenant


@router.post("/completions", response_model=ChatResponse)
async def chat_completions(
    req: ChatRequest,
    tenant=Depends(_get_tenant_from_header),
    db: AsyncSession = Depends(get_db),
    request: Request = None,
):
    """Send a chat completion request. Supports OpenAI and Anthropic models."""
    messages = [m.model_dump() for m in req.messages]

    result = await ai_service.chat(
        messages=messages,
        model=req.model,
        temperature=req.temperature,
        max_tokens=req.max_tokens,
    )

    cost = _cost_for_model(
        req.model,
        result["tokens"]["prompt"],
        result["tokens"]["completion"],
    )
    result["cost"] = round(cost, 6)

    # Record usage
    await tenant_service.record_api_call(
        db=db,
        tenant_id=tenant.id,
        endpoint="/api/v1/chat/completions",
        method="POST",
        status_code=200,
        tokens_used=result["tokens"]["total"],
        cost=result["cost"],
        response_time_ms=result["response_time_ms"],
    )

    return ChatResponse(
        content=result["content"],
        model=req.model,
        provider=result["provider"],
        tokens=result["tokens"],
        response_time_ms=round(result["response_time_ms"], 2),
    )


@router.post("/stream")
async def stream_chat(
    req: ChatRequest,
    tenant=Depends(_get_tenant_from_header),
):
    """Stream a chat completion (Server-Sent Events)."""
    if not req.stream:
        req.stream = True

    messages = [m.model_dump() for m in req.messages]

    return StreamingResponse(
        ai_service.stream_chat(
            messages=messages,
            model=req.model,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        ),
        media_type="text/event-stream",
    )
