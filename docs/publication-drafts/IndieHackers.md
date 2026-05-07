How I'm approaching AI SaaS with an open-source-first strategy

After building AI features for multiple products, I noticed a pattern: 80% of the code is always the same (auth, billing, rate limiting, usage tracking). The actual AI differentiator is only 20%.

So I extracted the 80% and open-sourced it as AI SaaS Kit:

https://github.com/crazycompanyinc/ai-saas-kit

The play:
1. Give away the infrastructure layer as MIT-licensed open-source
2. Build community trust and get contributions
3. Sell Pro: React dashboard, priority support, enterprise features
4. The repo itself generates leads - every star is a potential customer

What's included:
- Multi-tenant API (FastAPI + Python 3.11+)
- OpenAI + Anthropic unified interface
- Usage tracking with real-time cost calculation
- Token bucket rate limiting (Redis + in-memory)
- Stripe billing (Checkout, webhooks, subscriptions)
- Prompt template engine
- SSE streaming
- Docker deployment
- Full test suite (28+ tests passing)

Sponsors enabled - if this saves you time, a sponsorship is the best way to say thanks and keep development going.

I'm curious how other IHers approach the open-source vs paid split for developer tools. What's worked for you?