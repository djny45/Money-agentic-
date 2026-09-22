"use client";
import { useEffect, useState } from "react";
const integrations = [["CPA Network","cpagrip"],["Postiz","postiz"],["Bluesky","bluesky"],["Mastodon","mastodon"],["Ollama","ollama"]];
export default function Home() {
  const [status,setStatus]=useState({agent:"loading",publishing:"loading"});
  const [connected,setConnected]=useState({});
  useEffect(()=>{Promise.all([fetch("/api/status").then(r=>r.json()),fetch("/api/integrations").then(r=>r.json())]).then(([s,i])=>{setStatus(s);setConnected(Object.fromEntries(i.integrations.map(x=>[x.name,x.configured])))}).catch(()=>setStatus({agent:"offline",publishing:"unavailable"}))},[]);
  return <main className="shell">
    <nav><strong>Money-Agentic</strong><span>CPA Intelligence OS</span></nav>
    <section className="hero"><div><p className="eyebrow">AUTONOMOUS CAMPAIGN INTELLIGENCE</p><h1>One landing page.<br/>One control center.</h1><p className="sub">Connect authorized APIs, manage campaigns, observe real conversion data and let the swarm improve strategies from evidence.</p><button>DRY RUN</button></div><div className="orb"><div className="core"></div><i></i><i></i><i></i></div></section>
    <section className="grid"><article><small>CAMPAIGNS</small><b>—</b><span>Waiting for campaign data</span></article><article><small>CONVERSIONS</small><b>—</b><span>Real data only</span></article><article><small>REVENUE</small><b>—</b><span>Connected-source data</span></article><article><small>AGENT STATUS</small><b>{status.agent?.toUpperCase()}</b><span>{status.publishing}</span></article></section>
    <section className="panel"><div className="heading"><div><p className="eyebrow">API CONTROL CENTER</p><h2>Connect everything here</h2></div><span className="pill">SECRETS STAY SERVER-SIDE</span></div><div className="apis">{integrations.map(([name,key])=><div className="api" key={key}><div className={connected[name]?"dot live":"dot"}></div><div><strong>{name}</strong><span>{connected[name]?"Configured":"Not configured"}</span></div><code>{key}</code><button className="connect" disabled>{connected[name]?"Connected":"Configure on server"}</button></div>)}</div></section>
    <section className="panel"><div className="heading"><div><p className="eyebrow">SWARM</p><h2>Agent pipeline</h2></div></div><div className="pipeline">{["Research","Offer Intelligence","Content","Compliance","Publish Queue","Analytics","Learning"].map((x,i)=><div key={x}><em>{String(i+1).padStart(2,"0")}</em><span>{x}</span></div>)}</div></section>
  </main>;
}