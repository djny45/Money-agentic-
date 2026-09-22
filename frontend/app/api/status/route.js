import { NextResponse } from "next/server";

export async function GET() {
  const backend = process.env.PYTHON_API_URL;
  if (backend) {
    try {
      const response = await fetch(
        backend.replace(/\/$/, "") + "/api/status",
        { cache: "no-store" }
      );
      if (response.ok) {
        const data = await response.json();
        return NextResponse.json({
          mode: process.env.MODE || "DRY_RUN",
          autoPublish: process.env.AUTO_PUBLISH === "true",
          approvalRequired: process.env.AUTO_PUBLISH !== "true",
          integrations: Object.entries(data.integrations || {}).map(([name, configured]) => ({ name, configured })),
          backendConnected: true
        });
      }
    } catch {}
  }

  const providers = {
    cpagrip: ["CPAGRIP_API_KEY", "CPAGRIP_API_URL"],
    postiz: ["POSTIZ_API_KEY", "POSTIZ_API_URL"],
    bluesky: ["BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD"],
    mastodon: ["MASTODON_ACCESS_TOKEN", "MASTODON_BASE_URL"],
    llm_api: ["LLM_API_KEY", "LLM_API_URL", "LLM_MODEL"]
  };
  return NextResponse.json({
    mode: process.env.MODE || "DRY_RUN",
    autoPublish: process.env.AUTO_PUBLISH === "true",
    approvalRequired: process.env.AUTO_PUBLISH !== "true",
    integrations: Object.entries(providers).map(([name, vars]) => ({
      name, configured: vars.every((key) => Boolean(process.env[key]))
    })),
    backendConnected: false
  });
}
