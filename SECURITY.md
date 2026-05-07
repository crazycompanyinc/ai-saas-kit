# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x.x   | ✅        |

## Reporting a Vulnerability

If you discover a security vulnerability in AI SaaS Kit, please report it by opening a [GitHub Issue](https://github.com/crazycompanyinc/ai-saas-kit/issues) with the label `security`.

We will acknowledge your report within 48 hours and provide a timeline for a fix.

Please **do not** disclose vulnerabilities publicly until we have addressed them.

## Security Best Practices

When deploying AI SaaS Kit:

- **Never commit `.env` files** — API keys and secrets should be managed via environment variables
- **Use HTTPS in production** — always deploy behind a TLS-terminating reverse proxy
- **Rotate API keys regularly** — use the tenant management endpoints to regenerate keys
- **Set strong `SECRET_KEY`** — used for JWT signing, should be a random 64+ char string
- **Use PostgreSQL in production** — SQLite is provided for development only
- **Enable Redis** for production rate limiting to prevent distributed abuse
