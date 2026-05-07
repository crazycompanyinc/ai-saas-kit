import Stripe from "stripe";

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2024-04-10" as any,
});

export const PLANS = {
  STARTER: {
    name: "Starter",
    priceId: process.env.STRIPE_PRICE_STARTER!,
    price: 49,
    features: ["Auth (GitHub, Google, Email)", "Stripe billing", "Dashboard", "UI Components", "Dark mode", "Responsive"],
  },
  PRO: {
    name: "Pro",
    priceId: process.env.STRIPE_PRICE_PRO!,
    price: 99,
    features: [
      "Everything in Starter",
      "AI Integrations (OpenAI, Anthropic)",
      "Landing Page",
      "Email (Resend)",
      "Blog/MDX",
      "Admin Panel",
      "15+ Advanced UI Components",
      "Priority support",
    ],
  },
} as const;

export type PlanType = keyof typeof PLANS;

export async function createCheckoutSession(
  plan: PlanType,
  customerEmail: string,
  userId: string
) {
  return stripe.checkout.sessions.create({
    mode: "subscription",
    customer_email: customerEmail,
    line_items: [{ price: PLANS[plan].priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    metadata: { userId, plan },
  });
}

export async function createPortalSession(stripeCustomerId: string) {
  return stripe.billingPortal.sessions.create({
    customer: stripeCustomerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard`,
  });
}
