import { auth } from "@/lib/auth";
import { createPortalSession } from "@/lib/stripe";
import { db } from "@/lib/db";
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const session = await auth();
    if (!session?.user) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const user = await db.user.findUnique({ where: { id: session.user.id } });
    if (!user?.stripeId) {
      return NextResponse.json({ error: "No subscription found" }, { status: 400 });
    }

    const portalSession = await createPortalSession(user.stripeId);
    return NextResponse.json({ url: portalSession.url });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
