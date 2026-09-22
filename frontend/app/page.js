"use client";
import { useEffect, useState } from "react";

const integrations = [["CPA Network","cpagrip"],["Postiz","postiz"],["Bluesky","bluesky"],["Mastodon","mastodon"],["LLM API","llm_api"]];

export default function Home() {
  const [status,setStatus] = useState({agent:"loading",publishing:"loading",mode:"DRY_RUN"});
  const [connected,setConnected] = useState({});
  const [metrics,setMetrics] = useState({impressions:0,clicks:0,conversions:0,revenue:0,profit:0,epc:0});

  useEffect(() => {
    Promise.all([fetch("/api/status").then(r=>r.json()),fetch("/api/analytics").then(r=>r.json())])
      .then(([s,a]) => {
        setStatus({...s,agent:"ready",publishing:s.approvalRequired ? "approval_required" : "enabled"});
        setConnected(Object.fromEntries((s.integrations||[]).map(x=>[x.name,x.configured])));
        setMetrics(a); refreshAutomation();
      }).catch(()=>setStatus({agent:"offline",publishing:"unavailable",mode:"UNKNOWN"}));
  }, []);

  return <main className="shell">
    <nav><strong>Money-Agentic</strong><span>CPA Intelligence OS</span></nav>
    <section className="hero"><div>
      <p className="eyebrow">AUTONOMOUS CAMPAIGN INTELLIGENCE</p>
      <h1>One landing page.<br/>One control center.</h1>
      <p className="sub">Connect authorized APIs, manage campaigns, observe real conversion data and let the swarm improve strategies from evidence.</p>
      <button>{status.mode}</button>
    </div><div className="orb"><div className="core"></div><i></i><i></i><i></i></div></section>
    <section className="grid">
      <article><small>CLICKS</small><b>{metrics.clicks}</b><span>Observed campaign data</span></article>
      <article><small>CONVERSIONS</small><b>{metrics.conversions}</b><span>Real conversions only</span></article>
      <article><small>REVENUE</small><b>{"$"}{Number(metrics.revenue||0).toFixed(2)}</b><span>Connected-source data</span></article>
      <article><small>AGENT STATUS</small><b>{status.agent?.toUpperCase()}</b><span>{status.publishing}</span></article>
    </section>
    <section className="panel"><div className="heading"><div><p className="eyebrow">PERFORMANCE</p><h2>Measured results</h2></div><span className="pill">NO FABRICATED METRICS</span></div>
      <div className="grid">
        <article><small>IMPRESSIONS</small><b>{metrics.impressions}</b></article>
        <article><small>PROFIT</small><b>{"$"}{Number(metrics.profit||0).toFixed(2)}</b></article>
        <article><small>EPC</small><b>{"$"}{Number(metrics.epc||0).toFixed(4)}</b></article>
      </div>
    </section>
    <section className="panel"><div className="heading"><div><p className="eyebrow">API CONTROL CENTER</p><h2>Connect everything here</h2></div><span className="pill">SECRETS STAY SERVER-SIDE</span></div>
      <div className="apis">{integrations.map(([name,key])=><div className="api" key={key}><div className={connected[key]?"dot live":"dot"}></div><div><strong>{name}</strong><span>{connected[key]?"Configured":"Not configured"}</span></div><code>{key}</code><button className="connect" disabled>{connected[key]?"Connected":"Configure on server"}</button></div>)}</div>
    </section>
    <section className="panel"><div className="heading"><div><p className="eyebrow">AUTOPILOT</p><h2>Campaign control loop</h2></div><button className="connect" disabled={running} onClick={async()=>{setRunning(true);try{await fetch("/api/autopilot/run",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({channel:"postiz",limit:5})});await refreshAutomation();}finally{setRunning(false);}}}>{running?"Running…":"Run autopilot"}</button></div>
      <p className="sub">Research, score, compliance-check and queue observed offers. Publishing remains approval-gated.</p>
      <div className="grid">
        <article><small>PENDING APPROVAL</small><b>{queue.length}</b><span>Drafts waiting for review</span></article>
        <article><small>AUTOMATION RUNS</small><b>{runs.length}</b><span>Recorded control cycles</span></article>
        <article><small>LAST RUN</small><b>{runs[0]?.queued ?? 0}</b><span>Items queued</span></article>
      </div>
      {queue.slice(0,5).map(item=><div className="api" key={item.id}><div><strong>{item.channel}</strong><span>{item.text}</span></div><code>#{item.id}</code></div>)}
    </section>
    <section className="panel"><div className="heading"><div><p className="eyebrow">SWARM</p><h2>Agent pipeline</h2></div></div>
      <div className="pipeline">{["Research","Offer Intelligence","Content","Compliance","Publish Queue","Analytics","Learning"].map((x,i)=><div key={x}><em>{String(i+1).padStart(2,"0")}</em><span>{x}</span></div>)}</div>
    </section>
  </main>;
}
