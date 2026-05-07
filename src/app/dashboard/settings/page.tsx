import { redirect } from "next/navigation"
import { auth } from "@/lib/auth"
import { db } from "@/lib/db"
import { signOut } from "@/lib/auth"

export default async function SettingsPage() {
  const session = await auth()
  if (!session) redirect("/login")

  const user = await db.user.findUnique({ where: { id: session.user.id } })

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-muted-foreground mt-1">Manage your account settings</p>
      </div>

      {/* Profile */}
      <div className="bg-card border rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-4">Profile</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Name</label>
            <input
              type="text"
              defaultValue={user?.name || ""}
              placeholder="Your name"
              className="w-full max-w-sm h-10 px-3 rounded-md border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input
              type="email"
              defaultValue={user?.email || ""}
              disabled
              className="w-full max-w-sm h-10 px-3 rounded-md border bg-muted text-sm text-muted-foreground"
            />
            <p className="text-xs text-muted-foreground mt-1">Email cannot be changed</p>
          </div>
          <button className="bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-4 rounded-md text-sm font-medium transition-colors">
            Save Changes
          </button>
        </div>
      </div>

      {/* Account Info */}
      <div className="bg-card border rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-4">Account</h2>
        <div className="space-y-3 text-sm">
          <div className="flex justify-between">
            <span className="text-muted-foreground">Plan</span>
            <span className="font-medium">{user?.plan || "FREE"}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">Member since</span>
            <span className="font-medium">
              {user?.createdAt.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">User ID</span>
            <span className="font-mono text-xs text-muted-foreground">{user?.id}</span>
          </div>
        </div>
      </div>

      {/* Danger Zone */}
      <div className="bg-card border border-destructive/20 rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-2 text-destructive">Danger Zone</h2>
        <p className="text-muted-foreground text-sm mb-4">
          Sign out of your account on this device.
        </p>
        <form
          action={async () => {
            "use server"
            await signOut({ redirectTo: "/" })
          }}
        >
          <button
            type="submit"
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90 h-9 px-4 rounded-md text-sm font-medium transition-colors"
          >
            Sign Out
          </button>
        </form>
      </div>
    </div>
  )
}
