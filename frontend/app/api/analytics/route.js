import { NextResponse } from "next/server";

export async function GET() {
  const backend = process.env.PYTHON_API_URL;
  if (!backend) {
    return NextResponse.json({
      impressions: 0, clicks: 0, conversions: 0, revenue: 0,
      spend: 0, profit: 0, ctr: 0, conversion_rate: 0, epc: 0,
      source: "SQLite experiment data",
      connected: false
    });
  }

  try {
    const response = await fetch(
      backend.replace(/\/$/, "") + "/api/analytics",
      { cache: "no-store" }
    );
    if (!response.ok) throw new Error("backend unavailable");
    return NextResponse.json({ ...(await response.json()), connected: true });
  } catch {
    return NextResponse.json({
      impressions: 0, clicks: 0, conversions: 0, revenue: 0,
      spend: 0, profit: 0, ctr: 0, conversion_rate: 0, epc: 0,
      source: "SQLite experiment data",
      connected: false
    });
  }
}
