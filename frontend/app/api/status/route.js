import { NextResponse } from "next/server";

export async function GET() {
  const providers = {
    cpagrip: ["CPAGRIP_API_KEY", "CPAGRIP_API_URL"],
    postiz: ["POSTIZ_API_KEY", "POSTIZ_API_URL"],
    bluesky: ["BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD"],
    mastodon: ["MASTODON_ACCESS_TOKEN", "MASTODON_BASE_URL"],
    ollama: ["OLLAMA_URL", "OLLAMA_MODEL"]
  };
  const integrations = Object.entries(providers).map(([name, vars]) => ({
    name,
    configured: vars.every((key) => Boolean(process.env[key]))
  }));
  return NextResponse.json({
    mode: process.env.MODE || "DRY_RUN",
    autoPublish: process.env.AUTO_PUBLISH === "true",
    approvalRequired: process.env.AUTO_PUBLISH !== "true",
    integrations
  });
}
