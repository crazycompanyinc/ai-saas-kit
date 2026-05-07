"""Tests for AI SaaS Kit."""

import pytest
from httpx import AsyncClient, ASGITransport

from app import create_app


@pytest.fixture
def app():
    """Create test application."""
    return create_app()


@pytest.fixture
async def client(app):
    """Create async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def tenant_client(client, app):
    """Create a test tenant and return client + api_key."""
    # For tests, we need to bypass the DB dependency
    # We'll use the app with test config
    from app.core.security import generate_api_key
    api_key = generate_api_key()
    return {"client": client, "api_key": api_key}


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health endpoint returns healthy status."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.asyncio
async def test_openapi_docs(client):
    """Test that OpenAPI docs are accessible."""
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_openapi_schema(client):
    """Test that OpenAPI schema is valid."""
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert "/api/v1/tenants" in schema["paths"]
    assert "/api/v1/chat/completions" in schema["paths"]
    assert "/api/v1/usage/summary" in schema["paths"]
    assert "/api/v1/prompts" in schema["paths"]


class TestSecurity:
    """Test security utilities."""

    def test_generate_api_key(self):
        from app.core.security import generate_api_key
        key = generate_api_key()
        assert key.startswith("ak_")
        assert len(key) > 10

    def test_hash_api_key(self):
        from app.core.security import hash_api_key, generate_api_key
        key = generate_api_key()
        hashed = hash_api_key(key)
        assert len(hashed) == 64  # SHA-256 hex
        assert hashed != key

    def test_verify_api_key(self):
        from app.core.security import generate_api_key, hash_api_key, verify_api_key
        key = generate_api_key()
        hashed = hash_api_key(key)
        assert verify_api_key(key, hashed) is True
        assert verify_api_key("wrong_key", hashed) is False

    def test_jwt_token(self):
        from app.core.security import create_access_token, decode_access_token
        token = create_access_token({"sub": "test@example.com"})
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["sub"] == "test@example.com"

    def test_jwt_invalid_token(self):
        from app.core.security import decode_access_token
        decoded = decode_access_token("invalid.token.here")
        assert decoded is None


class TestRateLimiter:
    """Test in-memory rate limiter."""

    def test_allows_under_limit(self):
        from app.core.rate_limit import InMemoryRateLimiter
        limiter = InMemoryRateLimiter()
        for _ in range(10):
            assert limiter.is_allowed("test_key", max_requests=10, window=60) is True

    def test_blocks_over_limit(self):
        from app.core.rate_limit import InMemoryRateLimiter
        limiter = InMemoryRateLimiter()
        for _ in range(10):
            limiter.is_allowed("test_key", max_requests=10, window=60)
        assert limiter.is_allowed("test_key", max_requests=10, window=60) is False

    def test_separate_keys(self):
        from app.core.rate_limit import InMemoryRateLimiter
        limiter = InMemoryRateLimiter()
        for _ in range(10):
            limiter.is_allowed("key1", max_requests=10, window=60)
        # key2 should still be allowed
        assert limiter.is_allowed("key2", max_requests=10, window=60) is True


class TestConfig:
    """Test settings configuration."""

    def test_default_settings(self):
        from app.core.config import settings
        assert settings.APP_NAME == "AI SaaS Kit"
        assert settings.RATE_LIMIT_REQUESTS == 100
        assert settings.RATE_LIMIT_WINDOW == 3600

    def test_database_url_default(self):
        from app.core.config import settings
        assert "sqlite" in settings.DATABASE_URL


class TestModels:
    """Test SQLAlchemy models."""

    def test_tenant_model(self):
        from app.models import Tenant
        t = Tenant(name="Test", slug="test", api_key_hash="abc123")
        assert t.name == "Test"
        assert t.plan == "free"
        assert t.is_active is True

    def test_usage_record_model(self):
        from app.models import UsageRecord
        ur = UsageRecord(tenant_id=1, date="2026-01-01")
        assert ur.total_requests == 0
        assert ur.total_tokens == 0
        assert ur.total_cost == 0.0

    def test_prompt_template_model(self):
        from app.models import PromptTemplate
        pt = PromptTemplate(
            tenant_id=1,
            name="Test Prompt",
            slug="test-prompt",
            template="Hello {name}",
        )
        assert pt.name == "Test Prompt"
        assert pt.is_public is False
