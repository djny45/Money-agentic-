import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    mode: process.env.MODE || "DRY_RUN",
    agent: "ready",
    timestamp: new Date().toISOString(),
    publishing: process.env.AUTO_PUBLISH === "true" ? "enabled" : "approval_required"
  });
}