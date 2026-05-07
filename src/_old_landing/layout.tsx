import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI SaaS Kit — Ship your SaaS in hours, not weeks",
  description: "Production-ready Next.js starter with Auth, Stripe billing, AI integrations, and beautiful UI components.",
};

export default function LandingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
