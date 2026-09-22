import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    impressions: 0,
    clicks: 0,
    conversions: 0,
    revenue: 0,
    spend: 0,
    source: "connected campaign data"
  });
}