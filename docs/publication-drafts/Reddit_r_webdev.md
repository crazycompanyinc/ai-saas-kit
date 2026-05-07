I open-sourced a FastAPI starter kit for AI-powered SaaS - feedback welcome

Built this after realizing I was copy-pasting the same auth/usage/billing code across projects every single time.

AI SaaS Kit - production-ready, MIT licensed:

- Multi-tenant API (API key auth)
- OpenAI + Anthropic unified interface
- Usage tracking with per-request cost calculation
- Rate limiting (token bucket, Redis + fallback)
- Stripe billing integration
- Prompt template management
- Streaming chat (SSE)
- Docker + docker-compose
- Full test suite (pytest + async)
- Python 3.11+, FastAPI, SQLAlchemy 2.0 async

Quick start:

  git clone https://github.com/crazycompanyinc/ai-saas-kit
  cd ai-saas-kit
  pip install -e ".[dev]"
  cp .env.example .env
  python run.py

API docs at http://localhost:8000/docs

Repo: https://github.com/crazycompanyinc/ai-saas-kit

What features would you want in a starter like this? I'm especially interested in what AI provider abstractions people actually need.