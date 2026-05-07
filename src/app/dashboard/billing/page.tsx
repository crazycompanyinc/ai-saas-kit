import { redirect } from "next/navigation"
import { auth } from "@/lib/auth"
import { db } from "@/lib/db"
import { PLANS } from "@/lib/stripe"

export default async function BillingPage() {
  const session = await auth()
  if (!session) redirect("/login")

  const user = await db.user.findUnique({ where: { id: session.user.id } })
  const currentPlan = user?.plan || "FREE"
  const planInfo = currentPlan !== "FREE" ? PLANS[currentPlan as keyof typeof PLANS] : null

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Billing</h1>
        <p className="text-muted-foreground mt-1">Manage your subscription and billing</p>
      </div>

      {/* Current Plan */}
      <div className="bg-card border rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-4">Current Plan</h2>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-2xl font-bold">
              {currentPlan === "FREE" ? "Free" : planInfo?.name || currentPlan}
            </p>
            {planInfo ? (
              <p className="text-muted-foreground text-sm">${planInfo.price} one-time</p>
            ) : (
              <p className="text-muted-foreground text-sm">No active subscription</p>
            )}
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-medium ${
            currentPlan === "PRO"
              ? "bg-primary text-primary-foreground"
              : currentPlan === "STARTER"
              ? "bg-secondary text-secondary-foreground"
              : "bg-muted text-muted-foreground"
          }`}>
            {currentPlan}
          </span>
        </div>
      </div>

      {/* Upgrade Options */}
      {currentPlan === "FREE" && (
        <div className="bg-card border rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Upgrade Your Plan</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(PLANS).map(([key, plan]) => (
              <div key={key} className={`border rounded-lg p-6 ${key === "PRO" ? "ring-2 ring-primary" : ""}`}>
                {key === "PRO" && (
                  <span className="inline-block bg-primary text-primary-foreground text-xs font-medium px-3 py-1 rounded-full mb-3">
                    Most Popular
                  </span>
                )}
                <h3 className="text-lg font-bold">{plan.name}</h3>
                <p className="text-3xl font-bold mt-2">${plan.price}<span className="text-sm text-muted-foreground font-normal"> one-time</span></p>
                <ul className="mt-4 space-y-2">
                  {plan.features.map((f, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm">
                      <svg className="w-4 h-4 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      {f}
                    </li>
                  ))}
                </ul>
                <form action="/api/stripe/checkout" method="POST" className="mt-4">
                  <input type="hidden" name="plan" value={key} />
                  <button
                    type="submit"
                    className={`w-full h-10 rounded-md text-sm font-medium transition-colors ${
                      key === "PRO"
                        ? "bg-primary text-primary-foreground hover:bg-primary/90"
                        : "border hover:bg-muted"
                    }`}
                  >
                    Upgrade to {plan.name}
                  </button>
                </form>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Manage Subscription */}
      {currentPlan !== "FREE" && user?.stripeId && (
        <div className="bg-card border rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Manage Subscription</h2>
          <p className="text-muted-foreground text-sm mb-4">
            Use the Stripe Customer Portal to update payment methods, view invoices, or cancel.
          </p>
          <form action="/api/stripe/portal" method="POST">
            <button
              type="submit"
              className="border hover:bg-muted h-10 px-4 rounded-md text-sm font-medium transition-colors"
            >
              Open Customer Portal
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
