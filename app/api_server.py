from fastapi import FastAPI, HTTPException, Header
from .config import settings
from pydantic import BaseModel, Field
from .api_service import integration_status, search_openaffiliate, fetch_cpagrip_offers, create_postiz_draft
from .services import analytics, create_experiment, create_offer, get_experiment, get_offer, import_observed_offers, learning_decision, list_experiments, list_offers, record_metrics, tracked_offer_url
from .audit import list_audit, log_action
from .strategy import StrategyManager
from .publish_store import approve as approve_publish, enqueue as enqueue_publish, list_items as list_publish_items
from .autopilot import list_autopilot_runs, run_autopilot
from .optimizer import optimize_experiments
from .strategy_store import get_strategy, list_strategy_versions, rollback_strategy, save_strategy

app = FastAPI(title="Money-Agentic API", version="0.1.0")


def require_control_token(authorization: str | None) -> None:
    if not settings.control_token:
        raise HTTPException(status_code=503, detail="control token is not configured")
    if authorization != f"Bearer {settings.control_token}":
        raise HTTPException(status_code=401, detail="unauthorized")

class OfferIn(BaseModel):
    title: str
    url: str
    payout: float = Field(ge=0)
    country: str
    category: str | None = None
    offer_id: str | None = None

class ExperimentIn(BaseModel):
    offer_id: str
    channel: str
    variant: str
    experiment_id: str | None = None

class AutopilotIn(BaseModel):
    channel: str = Field(min_length=1, max_length=100)
    limit: int = Field(default=5, ge=1, le=20)


class QueuePublishIn(BaseModel):
    channel: str = Field(min_length=1, max_length=100)
    text: str = Field(min_length=1, max_length=10000)
    url: str = Field(min_length=1, max_length=4000)


class QueueApprovalIn(BaseModel):
    item_id: int = Field(ge=1)


class PostDraftIn(BaseModel):
    content: str = Field(min_length=1, max_length=10000)
    integration_ids: list[str] = Field(min_length=1, max_length=20)
    scheduled_at: str


class StrategyIn(BaseModel):
    offer_title: str
    channel: str

class RollbackIn(BaseModel):
    version: int = Field(ge=1)

class MetricsIn(BaseModel):
    impressions: int = Field(default=0, ge=0)
    clicks: int = Field(default=0, ge=0)
    conversions: int = Field(default=0, ge=0)
    revenue: float = Field(default=0, ge=0)
    spend: float = Field(default=0, ge=0)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "money-agentic"}

@app.get("/api/status")
async def status():
    return {"mode": settings.mode, "auto_publish": settings.auto_publish, "approval_required": not settings.auto_publish, "integrations": integration_status()}

@app.get("/api/analytics")
async def api_analytics():
    return await analytics()

@app.get("/api/offers")
async def offers():
    return await list_offers()

@app.post("/api/offers")
async def add_offer(payload: OfferIn, authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    result = await create_offer(**payload.model_dump())
    await log_action("offer_created", target=result["id"], details={"country": result["country"], "category": result.get("category")})
    return result

@app.get("/api/offers/{offer_id}")
async def offer(offer_id: str):
    result = await get_offer(offer_id)
    if not result:
        raise HTTPException(status_code=404, detail="offer not found")
    return result

@app.get("/api/experiments")
async def experiments():
    return await list_experiments()

@app.post("/api/experiments")
async def add_experiment(payload: ExperimentIn, authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    if not await get_offer(payload.offer_id):
        raise HTTPException(status_code=404, detail="offer not found")
    result = await create_experiment(**payload.model_dump())
    await log_action("experiment_created", target=result["id"], details={"offer_id": result["offer_id"], "channel": result["channel"], "variant": result["variant"]})
    return result

@app.post("/api/experiments/{experiment_id}/metrics")
async def metrics(experiment_id: str, payload: MetricsIn, authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    if not await get_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="experiment not found")
    result = await record_metrics(experiment_id, **payload.model_dump())
    await log_action("metrics_recorded", target=experiment_id, details=payload.model_dump())
    return result

@app.get("/api/experiments/{experiment_id}/learning")
async def learning(experiment_id: str):
    result = await learning_decision(experiment_id)
    if not result:
        raise HTTPException(status_code=404, detail="experiment not found")
    return result

@app.get("/api/offers/{offer_id}/tracked-url")
async def tracked_url(offer_id: str, source: str, medium: str, campaign: str, content: str | None = None):
    result = await tracked_offer_url(offer_id, source=source, medium=medium, campaign=campaign, content=content)
    if not result:
        raise HTTPException(status_code=404, detail="offer not found")
    return {"url": result}


@app.post("/api/research/import-cpagrip")
async def import_cpagrip(authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    rows = await fetch_cpagrip_offers()
    imported = await import_observed_offers(rows)
    await log_action("cpagrip_import", details={"observed": len(rows), "imported": len(imported)})
    return {"imported": imported, "observed": len(rows)}

@app.post("/api/autopilot/run")
async def autopilot_run(payload: AutopilotIn, authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    result = await run_autopilot(channel=payload.channel, limit=payload.limit)
    await log_action(
        "autopilot_run",
        target=str(result["run_id"]),
        details={
            "channel": payload.channel,
            "scanned": result["scanned"],
            "queued": result["queued"],
            "blocked": result["blocked"],
        },
    )
    return result


@app.post("/api/autopilot/optimize")
async def autopilot_optimize(authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    result = await optimize_experiments(sample_floor=settings.min_experiment_sample)
    await log_action(
        "autopilot_optimize",
        details={
            "evaluated": result["evaluated"],
            "promoted": result["promoted"],
            "revised": result["revised"],
            "paused": result["paused"],
        },
    )
    return result


@app.get("/api/autopilot/runs")
async def autopilot_runs(limit: int = 20):
    return {"runs": await list_autopilot_runs(limit)}


@app.post("/api/publishing/queue")
async def queue_publish(payload: QueuePublishIn, authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    result = await enqueue_publish(payload.channel, payload.text, payload.url)
    await log_action("publish_queued", target=str(result["id"]), details={"channel": payload.channel})
    return result


@app.get("/api/publishing/queue")
async def publishing_queue(status: str | None = None):
    return {"items": await list_publish_items(status)}


@app.post("/api/publishing/queue/approve")
async def approve_publish_item(payload: QueueApprovalIn, authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    result = await approve_publish(payload.item_id)
    if not result:
        raise HTTPException(status_code=404, detail="queue item not found")
    if result["status"] != "approved":
        raise HTTPException(status_code=409, detail="queue item is not pending")
    await log_action("publish_approved", target=str(payload.item_id))
    return result


@app.post("/api/publishing/postiz-draft")
async def postiz_draft(payload: PostDraftIn, authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    result = await create_postiz_draft(payload.content, payload.integration_ids, payload.scheduled_at)
    await log_action("postiz_draft_requested", details={"integration_count": len(payload.integration_ids), "status": result.get("status")})
    return result


@app.post("/api/strategies/propose")
async def propose_strategy(payload: StrategyIn, authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    strategy = StrategyManager().propose(payload.offer_title, payload.channel)
    result = await save_strategy(strategy)
    await log_action("strategy_saved", target=result["name"], details={"version": result["version"]})
    return result

@app.get("/api/strategies/{name}")
async def strategy(name: str):
    result = await get_strategy(name)
    if not result:
        raise HTTPException(status_code=404, detail="strategy not found")
    return result

@app.get("/api/strategies/{name}/versions")
async def strategy_versions(name: str):
    return {"versions": await list_strategy_versions(name)}

@app.post("/api/strategies/{name}/rollback")
async def strategy_rollback(name: str, payload: RollbackIn, authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    result = await rollback_strategy(name, payload.version)
    if not result:
        raise HTTPException(status_code=404, detail="strategy version not found")
    await log_action("strategy_rollback", target=name, details={"source_version": payload.version, "new_version": result["version"]})
    return result

@app.get("/api/audit")
async def audit(limit: int = 100, authorization: str | None = Header(default=None)):
    require_control_token(authorization)
    return {"entries": await list_audit(limit)}

@app.get("/api/research/cpagrip-offers")
async def cpagrip_offers():
    return {"source": "configured CPAGrip feed", "offers": await fetch_cpagrip_offers()}

@app.get("/api/research/affiliate-programs")
async def affiliate_programs(q: str = "", category: str | None = None, commission_type: str | None = None, verified: bool | None = None):
    return {"source": "OpenAffiliate", "programs": await search_openaffiliate(q, category, commission_type, verified)}
