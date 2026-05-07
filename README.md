# 🚀 AI SaaS Kit

<div align="center">

[![Stars](https://img.shields.io/github/stars/crazycompanyinc/ai-saas-kit?style=social)](https://github.com/crazycompanyinc/ai-saas-kit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38B2AC?logo=tailwind-css)](https://tailwindcss.com/)
[![Prisma](https://img.shields.io/badge/Prisma-6-2D3748?logo=prisma)](https://www.prisma.io/)

**Ship your SaaS in hours, not weeks.**

Production-ready Next.js 15 starter with Auth, Stripe billing, AI integrations,
and beautiful UI components. Stop building boilerplate — start building your product.

[Demo](https://ai-saas-kit.dev) · [Docs](https://github.com/crazycompanyinc/ai-saas-kit#readme) · [Report Bug](https://github.com/crazycompanyinc/ai-saas-kit/issues)

</div>

---

## ✨ Features

### 🔐 Authentication — Ready out of the box
- **NextAuth.js v5** (Auth.js) with App Router
- **GitHub OAuth** — one-click sign in
- **Google OAuth** — Gmail-based auth
- **Magic Link** — passwordless email via Resend

### 💳 Billing & Subscriptions — Monetize from day one
- **Stripe Checkout** — hosted payment page
- **Stripe Customer Portal** — self-service billing management
- **Webhook handling** — automatic subscription lifecycle
- **Three-tier plans** — Free / Starter / Pro with feature gating

### 🤖 AI Integrations — Ship AI features fast
- **OpenAI API** — chat endpoint with streaming
- **Chat UI component** — ready-to-use conversational interface
- **Anthropic template** — Claude integration scaffold

### 🎨 UI Components — Beautiful by default
- **shadcn/ui** — pre-installed and configured
- **Dark / Light mode** — with next-themes
- **Responsive design** — mobile, tablet, desktop
- **Dashboard layout** — sidebar navigation, stats cards
- **Landing page** — hero, features, pricing table, CTA

### 📄 Pages Included

| Page | Description |
|------|-------------|
| `/` | Landing page with hero, features, pricing, CTA |
| `/login` | Sign in (GitHub, Google, magic link) |
| `/register` | Sign up (GitHub, Google, magic link) |
| `/dashboard` | Main dashboard with stats and quick actions |
| `/dashboard/billing` | Subscription management and upgrade |
| `/dashboard/settings` | Profile, account info, sign out |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | [Next.js 15](https://nextjs.org/) (App Router) |
| Language | [TypeScript](https://www.typescriptlang.org/) (strict mode) |
| Auth | [NextAuth.js v5](https://authjs.dev/) |
| Database | SQLite (dev) / PostgreSQL (prod) via [Prisma](https://www.prisma.io/) |
| Payments | [Stripe](https://stripe.com/) |
| UI | [Tailwind CSS](https://tailwindcss.com/) + [shadcn/ui](https://ui.shadcn.com/) |
| Themes | [next-themes](https://github.com/pacocoursey/next-themes) |
| Email | [Resend](https://resend.com/) |
| AI | [OpenAI SDK](https://platform.openai.com/docs) |

---

## 🏁 Quick Start

```bash
# Clone the repo
git clone https://github.com/crazycompanyinc/ai-saas-kit.git my-saas
cd my-saas

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Fill in .env.local with your API keys

# Set up the database
npx prisma generate
npx prisma db push

# Start the dev server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) — you're live! 🎉

### Environment Variables

Copy `.env.example` to `.env.local` and fill in:

| Variable | Required | Description |
|----------|----------|-------------|
| `AUTH_SECRET` | ✅ | Generate with `openssl rand -base64 32` |
| `DATABASE_URL` | ✅ | `file:./dev.db` for local |
| `NEXT_PUBLIC_APP_URL` | ✅ | Your app URL |
| `AUTH_GITHUB_ID` | GitHub OAuth | GitHub OAuth App ID |
| `AUTH_GITHUB_SECRET` | GitHub OAuth | GitHub OAuth App Secret |
| `AUTH_GOOGLE_ID` | Google OAuth | Google OAuth Client ID |
| `AUTH_GOOGLE_SECRET` | Google OAuth | Google OAuth Client Secret |
| `STRIPE_SECRET_KEY` | Billing | Stripe secret key |
| `STRIPE_PUBLISHABLE_KEY` | Billing | Stripe publishable key |
| `STRIPE_WEBHOOK_SECRET` | Billing | Stripe webhook secret |
| `STRIPE_PRICE_STARTER` | Billing | Stripe price ID for Starter plan |
| `STRIPE_PRICE_PRO` | Billing | Stripe price ID for Pro plan |
| `OPENAI_API_KEY` | AI features | OpenAI API key |
| `RESEND_API_KEY` | Email | Resend API key |

---

## 🚀 Deployment

### Vercel (Recommended)

1. Push to GitHub
2. Import project in [Vercel](https://vercel.com/new)
3. Add environment variables
4. Deploy!

```bash
npx vercel
```

### Database for Production

Switch to PostgreSQL in production:

1. Update `DATABASE_URL` in `.env.local`
2. Change the datasource in `prisma/schema.prisma`:
   ```prisma
   datasource db {
     provider = "postgresql"
     url      = env("DATABASE_URL")
   }
   ```
3. Run `npx prisma db push`

---

## 📁 Project Structure

```
src/
├── app/
│   ├── (auth)/          # Auth routes (login, register)
│   ├── (dashboard)/     # Dashboard routes
│   └── api/             # API routes
│       ├── auth/        # NextAuth handlers
│       ├── stripe/      # Stripe checkout, webhooks, portal
│       └── ai/          # AI chat endpoint
├── components/
│   ├── ui/              # shadcn/ui components
│   ├── dashboard/       # Dashboard-specific components
│   └── landing/         # Landing page components
├── lib/
│   ├── auth.ts          # Auth configuration
│   ├── stripe.ts        # Stripe helpers & plan config
│   ├── ai.ts            # AI integration
│   ├── db.ts            # Prisma client
│   └── utils.ts         # Utility functions
├── hooks/               # Custom React hooks
├── styles/              # Global CSS
└── types/               # TypeScript types
```

## 💰 Monetization

AI SaaS Kit is designed to help you launch and monetize fast:

| Tier | Price | Includes |
|------|-------|----------|
| **Free** | $0 | Basic starter template |
| **Starter** | $49 one-time | Auth + Billing + Dashboard + UI Components + Dark mode |
| **Pro** | $99 one-time | Starter + AI integrations + Landing page + Email + Blog + Admin |

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit PRs.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

[MIT](LICENSE) — use it for personal or commercial projects. No attribution required.

## 💖 Sponsors

If this project helped you ship faster, consider [sponsoring](https://github.com/sponsors/crazycompanyinc) the work!

---

<div align="center">

Built with ❤️ by [crazycompanyinc](https://github.com/crazycompanyinc)

⭐ Star this repo if you find it helpful!

</div>
