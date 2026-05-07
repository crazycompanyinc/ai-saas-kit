<div align="center">

# 🚀 AI SaaS Kit

**Launch your AI-powered SaaS in minutes, not months.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg)](https://fastapi.tiangolo.com/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
[![GitHub stars](https://img.shields.io/github/stars/crazycompanyinc/ai-saas-kit?social)](https://github.com/crazycompanyinc/ai-saas-kit)
[![Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ff69b4?logo=github)](https://github.com/sponsors/crazycompanyinc)

Topics: `fastapi` · `python` · `ai` · `saas` · `open-source` · `multi-tenant` · `boilerplate` · `anthropic` · `openai` · `gpt-4` · `claude` · `api` · `starter-kit` · `stripe` · `billing` · `rate-limiting` · `async` · `docker`

[English](README.md) · [Documentación](docs/)

</div>

---

## ✨ What is AI SaaS Kit?

AI SaaS Kit is a **production-ready, open-source starter kit** for building AI-powered SaaS applications. It gives you everything you need to start charging for AI features from day one — multi-tenant API, usage tracking, rate limiting, billing integration, and more.

Stop reinventing the wheel. Focus on your unique AI features, not the boilerplate.

## 🤔 Why Open Source?

We believe the best way to build a great product is in the open. The core infrastructure — multi-tenant auth, usage tracking, rate limiting, AI provider abstraction — is something every AI SaaS needs. By open-sourcing it, we:

- **Help builders ship faster** — skip the boilerplate, focus on your unique value
- **Get community contributions** — more providers, more features, better tests
- **Build trust** — your customers can see exactly how their data is handled
- **Generate leads for Pro** — need the React dashboard, priority support, or enterprise features? [Check out the Pro version](#)

## 🎯 Key Features

| Feature | Description |
|---|---|
| 🤖 **Multi-Provider AI** | Unified API for OpenAI (GPT-4o, GPT-4o-mini) and Anthropic (Claude Sonnet, Claude Haiku) |
| 🏢 **Multi-Tenant** | Tenant management with API key authentication, isolated data per tenant |
| 📊 **Usage Tracking** | Per-request token tracking, cost calculation, daily aggregation, analytics dashboard |
| 💳 **Stripe Billing** | Ready for Stripe Checkout integration — subscription management, webhook handling |
| 🛡️ **Rate Limiting** | Token bucket rate limiter with Redis or in-memory fallback |
| 📝 **Prompt Templates** | CRUD for reusable prompt templates with variable substitution |
| 🔌 **Streaming** | Server-Sent Events (SSE) streaming for chat completions |
| 🐳 **Docker Ready** | Dockerfile and docker-compose included for one-command deployment |
| 🧪 **Tested** | Full test suite with pytest + async support |

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- An OpenAI or Anthropic API key

### Installation

```bash
# Clone the repository
git clone https://github.com/crazycompanyinc/ai-saas-kit.git
cd ai-saas-kit

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Run

```bash
# Start the development server
python run.py
```

The API will be available at `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

### Docker

```bash
docker compose up --build
```

## 📖 API Usage

### 1. Create a Tenant

```bash
curl -X POST http://localhost:8000/api/v1/tenants \
  -H "Content-Type: application/json" \
  -d '{"name": "My App", "slug": "my-app"}'
```

Response:
```json
{
  "id": 1,
  "name": "My App",
  "slug": "my-app",
  "plan": "free",
  "is_active": true,
  "api_key": "ak_XXXXXXXXXXXXXXXX"
}
```

> ⚠️ **Save the API key** — it's only shown once.

### 2. Chat Completion

```bash
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ak_XXXXXXXXXXXXXXXX" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "model": "gpt-4o-mini",
    "temperature": 0.7
  }'
```

Response:
```json
{
  "content": "Hello! How can I help you today?",
  "model": "gpt-4o-mini",
  "provider": "openai",
  "tokens": {"prompt": 10, "completion": 9, "total": 19},
  "response_time_ms": 452.31
}
```

### 3. Streaming Chat

```bash
curl -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ak_XXXXXXXXXXXXXXXX" \
  -d '{
    "messages": [{"role": "user", "content": "Tell me a story"}],
    "model": "gpt-4o-mini",
    "stream": true
  }'
```

### 4. Check Usage

```bash
curl http://localhost:8000/api/v1/usage/summary?days=30 \
  -H "X-API-Key: ak_XXXXXXXXXXXXXXXX"
```

## 🏗️ Architecture

```
ai-saas-kit/
├── app/
│   ├── __init__.py          # FastAPI app factory
│   ├── core/
│   │   ├── config.py        # Pydantic settings
│   │   ├── database.py      # SQLAlchemy async engine
│   │   ├── rate_limit.py    # Rate limiting middleware
│   │   └── security.py      # API key & JWT utilities
│   ├── api/
│   │   └── routes/
│   │       ├── chat.py      # Chat completions (sync + stream)
│   │       ├── tenants.py   # Tenant CRUD
│   │       ├── usage.py     # Usage analytics
│   │       └── prompts.py   # Prompt template management
│   ├── models/              # SQLAlchemy models
│   │   └── __init__.py      # Tenant, UsageRecord, ApiCall, PromptTemplate
│   └── services/
│       ├── ai_service.py    # Multi-provider AI abstraction
│       └── tenant_service.py # Tenant & usage management
├── tests/                   # Test suite
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
├── migrations/              # Database migrations
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## 🛠️ Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) — modern, async Python web framework
- **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) — async database access
- **Database:** SQLite (default) / PostgreSQL (production)
- **AI:** OpenAI API + Anthropic API
- **Billing:** [Stripe](https://stripe.com/) (optional)
- **Cache:** Redis (optional, falls back to in-memory)
- **Validation:** [Pydantic v2](https://docs.pydantic.dev/)
- **Auth:** API keys (SHA-256 hashed) + JWT support
- **Testing:** pytest + pytest-asyncio
- **Linting:** [Ruff](https://github.com/astral-sh/ruff)

## 📋 Roadmap

- [ ] User dashboard (React frontend)
- [ ] PostgreSQL support with Alembic migrations
- [ ] Redis-backed rate limiting
- [ ] Stripe webhook handlers
- [ ] Email notifications
- [ ] Admin panel
- [ ] More AI providers (Google Gemini, Mistral, etc.)
- [ ] SDK clients (Python, JavaScript)
- [ ] Kubernetes deployment configs

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`pytest`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 💖 Sponsors

If this project helps you build your SaaS faster, consider [becoming a sponsor](https://github.com/sponsors/crazycompanyinc)!

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ff69b4?logo=github)](https://github.com/sponsors/crazycompanyinc)

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ for the AI SaaS builder community.**

⭐ Star this repo if it helps you!

</div>
