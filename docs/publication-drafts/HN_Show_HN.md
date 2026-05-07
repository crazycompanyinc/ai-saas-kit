Show HN: AI SaaS Kit - Open-source starter kit for AI-powered SaaS (FastAPI + Python)

Hey HN! I built AI SaaS Kit because I was tired of rebuilding the same boilerplate every time I started a new AI project.

It's a production-ready FastAPI starter kit that gives you everything needed to start charging for AI features:

- Multi-tenant API with API key auth
- Unified interface for OpenAI (GPT-4o) and Anthropic (Claude)
- Per-request usage tracking with cost calculation
- Token bucket rate limiting (Redis + in-memory fallback)
- Stripe Checkout integration
- Prompt template management with variable substitution
- SSE streaming for chat completions
- Docker support, full test suite with pytest

The idea: release the core infrastructure as open-source to help builders ship faster, and generate leads for a Pro version with dashboard, priority support, and enterprise features.

Stack: Python 3.11+, FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Redis (optional), Stripe.

Repo: https://github.com/crazycompanyinc/ai-saas-kit

Would love feedback from anyone who's built AI SaaS products - what's missing? What would you change?