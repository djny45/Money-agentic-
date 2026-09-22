import { NextResponse } from "next/server";

const providers = {
  cpagrip: ["CPAGRIP_API_KEY", "CPAGRIP_API_URL"],
  postiz: ["POSTIZ_API_KEY", "POSTIZ_API_URL"],
  bluesky: ["BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD"],
  mastodon: ["MASTODON_ACCESS_TOKEN", "MASTODON_BASE_URL"],
  ollama: ["OLLAMA_URL", "OLLAMA_MODEL"]
};

export async function GET() {
  const integrations = Object.entries(providers).map(([name, vars]) => ({
    name,
    configured: vars.every((key) => Boolean(process.env[key]))
  }));
  return NextResponse.json({ integrations });
}