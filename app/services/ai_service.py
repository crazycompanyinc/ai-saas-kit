"""AI service — abstracts LLM providers (OpenAI, Anthropic, etc.)."""

import time
from typing import AsyncGenerator, Optional

import httpx

from app.core.config import settings


class AIService:
    """Multi-provider AI service with usage tracking."""

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=60.0)

    async def chat(
        self,
        messages: list[dict],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> dict:
        """Send a chat completion request."""
        if model.startswith("claude"):
            return await self._chat_anthropic(messages, model, temperature, max_tokens)
        return await self._chat_openai(messages, model, temperature, max_tokens)

    async def _chat_openai(
        self,
        messages: list[dict],
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> dict:
        """OpenAI chat completion."""
        start = time.time()
        response = await self._client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        )
        elapsed = (time.time() - start) * 1000
        data = response.json()

        usage = data.get("usage", {})
        return {
            "content": data["choices"][0]["message"]["content"],
            "model": model,
            "provider": "openai",
            "tokens": {
                "prompt": usage.get("prompt_tokens", 0),
                "completion": usage.get("completion_tokens", 0),
                "total": usage.get("total_tokens", 0),
            },
            "response_time_ms": elapsed,
            "status_code": response.status_code,
        }

    async def _chat_anthropic(
        self,
        messages: list[dict],
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> dict:
        """Anthropic chat completion."""
        start = time.time()

        # Convert messages to Anthropic format
        system_msg = ""
        anthropic_messages = []
        for m in messages:
            if m["role"] == "system":
                system_msg = m["content"]
            else:
                anthropic_messages.append(m)

        body = {
            "model": model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system_msg:
            body["system"] = system_msg

        response = await self._client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
            },
            json=body,
        )
        elapsed = (time.time() - start) * 1000
        data = response.json()

        content = data.get("content", [{}])
        usage = data.get("usage", {})
        return {
            "content": content[0].get("text", "") if content else "",
            "model": model,
            "provider": "anthropic",
            "tokens": {
                "prompt": usage.get("input_tokens", 0),
                "completion": usage.get("output_tokens", 0),
                "total": (usage.get("input_tokens", 0) + usage.get("output_tokens", 0)),
            },
            "response_time_ms": elapsed,
            "status_code": response.status_code,
        }

    async def stream_chat(
        self,
        messages: list[dict],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> AsyncGenerator[str, None]:
        """Stream a chat completion (OpenAI only for now)."""
        async with self._client.stream(
            "POST",
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True,
            },
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: ") and line.strip() != "data: [DONE]":
                    yield line

    async def close(self):
        await self._client.aclose()


ai_service = AIService()
