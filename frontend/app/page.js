"use client";

import { useState } from "react";

const integrations = [
  ["CPA Network", "CPAGRIP_API_KEY", "Offer and conversion data"],
  ["Postiz", "POSTIZ_API_KEY", "Authorized social publishing"],
  ["Bluesky", "BLUESKY_APP_PASSWORD", "Social publishing"],
  ["Mastodon", "MASTODON_ACCESS_TOKEN", "Social publishing"],
  ["Ollama", "OLLAMA_URL", "Local AI intelligence"]
];

export default function Home() {
  const [mode, setMode] = useState("DRY RUN");

  return (
    <main className="shell">
      <nav><strong>Money-Agentic</strong><span>CPA Intelligence OS</span></nav>
      <section className="hero">
        <div>
          <p className="eyebrow">AUTONOMOUS CAMPAIGN INTELLIGENCE</p>
          <h1>One landing page.<br/>One control center.</h1>
          <p className="sub">Connect your authorized APIs, manage campaigns, observe real conversion data and let the swarm improve strategies from evidence.</p>
          <button onClick={() => setMode(mode === "DRY RUN" ? "LIVE — APPROVAL REQUIRED" : "DRY RUN")}>{mode}</button>
        </div>
        <div className="orb"><div className="core"></div><i></i><i></i><i></i></div>
      </section>

      <section className="grid">
        <article><small>CAMPAIGNS</small><b>0</b><span>Waiting for integration</span></article>
        <article><small>CONVERSIONS</small><b>0</b><span>Real data only</span></article>
        <article><small>REVENUE</small><b>$0.00</b><span>Tracked from connected sources</span></article>
        <article><small>AGENT STATUS</small><b>READY</b><span>Learning loop initialized</span></article>
      </section>

      <section className="panel">
        <div className="heading"><div><p className="eyebrow">API CONTROL CENTER</p><h2>Connect everything here</h2></div><span className="pill">SECRETS STAY SERVER-SIDE</span></div>
        <div className="apis">
          {integrations.map(([name, env, purpose]) => (
            <div className="api" key={name}>
              <div className="dot"></div>
              <div><strong>{name}</strong><span>{purpose}</span></div>
              <code>{env}</code>
              <button className="connect">Configure</button>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="heading"><div><p className="eyebrow">SWARM</p><h2>Agent pipeline</h2></div></div>
        <div className="pipeline">
          {["Research","Offer Intelligence","Content","Compliance","Publish Queue","Analytics","Learning"].map((x, i) => <div key={x}><em>{String(i+1).padStart(2,"0")}</em><span>{x}</span></div>)}
        </div>
      </section>
    </main>
  );
}