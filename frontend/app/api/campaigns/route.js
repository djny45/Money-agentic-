import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "configured",
    message: "Campaign API is available through the Python service layer.",
    next: "/api/campaigns",
  });
}
