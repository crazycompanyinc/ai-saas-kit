# Changelog

All notable changes to AI SaaS Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-07

### Added

- **Multi-tenant API** with API key authentication (SHA-256 hashed)
- **Unified AI provider interface** supporting OpenAI (GPT-4o, GPT-4o-mini) and Anthropic (Claude Sonnet, Claude Haiku)
- **Usage tracking** — per-request token counting, cost calculation, daily aggregation
- **Rate limiting** — token bucket algorithm with Redis or in-memory fallback
- **Prompt template management** — CRUD operations with variable substitution
- **Streaming chat** — Server-Sent Events (SSE) for real-time completions
- **Stripe Checkout integration** — session creation, webhook handling, subscription management
- **Docker support** — Dockerfile + docker-compose.yml for one-command deployment
- **Full test suite** — pytest with async support, 28+ tests covering all endpoints
- **Open-source release** — MIT licensed with FUNDING.yml, contributing guidelines, code of conduct

### Tech Stack

- Python 3.11+, FastAPI, SQLAlchemy 2.0 (async), Pydantic v2
- SQLite (dev) / PostgreSQL (production), Redis (optional)
- Ruff for linting, pytest for testing
