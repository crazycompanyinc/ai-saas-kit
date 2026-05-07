import Link from "next/link";
import { PLANS } from "@/lib/stripe";

const features = [
  {
    icon: "⚡",
    title: "Ship in Hours, Not Weeks",
    description: "Production-ready codebase so you can focus on your unique features, not boilerplate.",
  },
  {
    icon: "🔐",
    title: "Auth Out of the Box",
    description: "GitHub, Google, and magic link authentication with NextAuth.js v5. Secure and fast.",
  },
  {
    icon: "💳",
    title: "Stripe Billing Ready",
    description: "Subscriptions, webhooks, and customer portal pre-configured. Start charging from day one.",
  },
  {
    icon: "🤖",
    title: "AI Integrations (Pro)",
    description: "OpenAI and Anthropic examples with ready-to-use API routes and chat UI components.",
  },
  {
    icon: "🎨",
    title: "Beautiful UI Components",
    description: "shadcn/ui components pre-installed. Dark mode, responsive, and accessible by default.",
  },
  {
    icon: "🚀",
    title: "Deploy to Vercel in 1 Click",
    description: "Optimized for Vercel deployment. Push to main and you're live.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      {/* Nav */}
      <nav className="border-b">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-bold">AI SaaS Kit</Link>
          <div className="flex items-center gap-4">
            <Link href="/login" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Sign in
            </Link>
            <Link
              href="/register"
              className="bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-4 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-muted rounded-full px-4 py-1.5 text-sm mb-6">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            v1.0 — Production Ready
          </div>
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight leading-tight">
            Ship your SaaS in
            <span className="bg-gradient-to-r from-primary to-purple-500 bg-clip-text text-transparent"> hours</span>,
            not weeks
          </h1>
          <p className="text-xl text-muted-foreground mt-6 max-w-2xl mx-auto">
            Production-ready Next.js starter with Auth, Stripe billing, AI integrations,
            and beautiful UI components. Stop building boilerplate, start building your product.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8">
            <Link
              href="/register"
              className="bg-primary text-primary-foreground hover:bg-primary/90 h-12 px-8 rounded-md text-lg font-medium transition-colors"
            >
              Get Started — $49
            </Link>
            <a
              href="#features"
              className="border hover:bg-muted h-12 px-8 rounded-md text-lg font-medium transition-colors flex items-center justify-center"
            >
              Learn more
            </a>
          </div>
          <p className="text-sm text-muted-foreground mt-4">One-time purchase. Lifetime updates. No subscription.</p>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 px-6 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">
            Everything you need to launch
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, i) => (
              <div key={i} className="bg-card border rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="text-3xl mb-4">{feature.icon}</div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">Simple, Transparent Pricing</h2>
          <p className="text-muted-foreground text-center mb-12">
            One-time purchase. Free updates forever.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl mx-auto">
            {Object.entries(PLANS).map(([key, plan]) => (
              <div
                key={key}
                className={`bg-card border rounded-lg p-8 ${key === "PRO" ? "ring-2 ring-primary" : ""}`}
              >
                {key === "PRO" && (
                  <div className="inline-block bg-primary text-primary-foreground text-xs font-medium px-3 py-1 rounded-full mb-4">
                    Most Popular
                  </div>
                )}
                <h3 className="text-xl font-bold">{plan.name}</h3>
                <div className="mt-2">
                  <span className="text-4xl font-bold">${plan.price}</span>
                  <span className="text-muted-foreground"> one-time</span>
                </div>
                <ul className="mt-6 space-y-2">
                  {plan.features.map((feature, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm">
                      <svg className="w-4 h-4 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>
                <Link
                  href="/register"
                  className={`mt-6 w-full flex items-center justify-center h-10 rounded-md text-sm font-medium transition-colors ${
                    key === "PRO"
                      ? "bg-primary text-primary-foreground hover:bg-primary/90"
                      : "border hover:bg-muted"
                  }`}
                >
                  Get {plan.name}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 bg-muted/30">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to ship?</h2>
          <p className="text-muted-foreground mb-8">
            Join hundreds of developers who use AI SaaS Kit to launch faster.
          </p>
          <Link
            href="/register"
            className="inline-flex items-center justify-center bg-primary text-primary-foreground hover:bg-primary/90 h-12 px-8 rounded-md text-lg font-medium transition-colors"
          >
            Get Started Now
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-muted-foreground">
            AI SaaS Kit — Built with Next.js, Stripe & Love
          </p>
          <div className="flex items-center gap-6 text-sm text-muted-foreground">
            <Link href="/login" className="hover:text-foreground transition-colors">Login</Link>
            <Link href="/register" className="hover:text-foreground transition-colors">Register</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
