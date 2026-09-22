from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .api_service import integration_status
from .services import analytics, create_experiment, create_offer, get_experiment, get_offer, learning_decision, list_experiments, list_offers, record_metrics, tracked_offer_url

app = FastAPI(title="Money-Agentic API", version="0.1.0")

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
    return {"integrations": integration_status()}

@app.get("/api/analytics")
async def api_analytics():
    return await analytics()

@app.get("/api/offers")
async def offers():
    return await list_offers()

@app.post("/api/offers")
async def add_offer(payload: OfferIn):
    return await create_offer(**payload.model_dump())

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
async def add_experiment(payload: ExperimentIn):
    if not await get_offer(payload.offer_id):
        raise HTTPException(status_code=404, detail="offer not found")
    return await create_experiment(**payload.model_dump())

@app.post("/api/experiments/{experiment_id}/metrics")
async def metrics(experiment_id: str, payload: MetricsIn):
    if not await get_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="experiment not found")
    return await record_metrics(experiment_id, **payload.model_dump())

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
