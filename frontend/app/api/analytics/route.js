import { NextResponse } from "next/server";

export async function GET() {
  const payload = {
    impressions: 0,
    clicks: 0,
    conversions: 0,
    revenue: 0,
    spend: 0,
    profit: 0,
    ctr: 0,
    conversion_rate: 0,
    epc: 0,
    source: "SQLite experiment data",
    note: "Live aggregation is exposed by the Python service layer.",
  };
  return NextResponse.json(payload);
}
