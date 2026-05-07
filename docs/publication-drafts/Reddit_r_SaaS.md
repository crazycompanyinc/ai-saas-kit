[Open Source] AI SaaS Kit - Stop rebuilding boilerplate for every AI project

I've built and sold AI features for multiple SaaS products. Every single time, I ended up rebuilding the same infrastructure: multi-tenant auth, usage tracking, rate limiting, billing integration.

So I open-sourced it.

AI SaaS Kit is a production-ready FastAPI + Python starter kit:

Feature | Description
--- | ---
Multi-Tenant API | API key auth, isolated data per tenant
Multi-Provider AI | OpenAI + Anthropic unified interface
Usage Tracking | Token-level cost calculation, daily aggregation
Rate Limiting | Token bucket with Redis or in-memory fallback
Stripe Billing | Checkout sessions, webhook handling, subscription management
Prompt Templates | CRUD with variable substitution
Streaming | SSE for chat completions
Docker | One-command deployment

MIT Licensed. Works with SQLite for dev, PostgreSQL for production.

My thesis: open-source the infrastructure layer where everyone has the same needs, build trust, and convert users to Pro for the dashboard/enterprise features.

Repo: https://github.com/crazycompanyinc/ai-saas-kit

Happy to answer any questions about the architecture or my experience building AI SaaS products.