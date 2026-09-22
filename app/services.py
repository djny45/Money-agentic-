from dataclasses import asdict
from datetime import datetime, timezone
import uuid

from .db import DB_PATH, init_db
from .tracking import add_utm
from .learning import LearningEngine
from .offer_intelligence import OfferIntelligence


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def create_offer(*, title: str, url: str, payout: float, country: str,
                       category: str | None = None, offer_id: str | None = None) -> dict:
    await init_db()
    offer_id = offer_id or str(uuid.uuid4())
    async with __import__("aiosqlite").connect(DB_PATH) as db:
        await db.execute(
            """INSERT OR REPLACE INTO offers
               (id,title,url,payout,country,category,conversion_rate,epc,active)
               VALUES (?,?,?,?,?,?,NULL,NULL,1)""",
            (offer_id, title, url, float(payout), country, category),
        )
        await db.commit()
    return await get_offer(offer_id)


async def get_offer(offer_id: str) -> dict | None:
    await init_db()
    async with __import__("aiosqlite").connect(DB_PATH) as db:
        db.row_factory = __import__("aiosqlite").Row
        cur = await db.execute("SELECT * FROM offers WHERE id=?", (offer_id,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def list_offers(active_only: bool = True) -> list[dict]:
    await init_db()
    async with __import__("aiosqlite").connect(DB_PATH) as db:
        db.row_factory = __import__("aiosqlite").Row
        sql = "SELECT * FROM offers"
        if active_only:
            sql += " WHERE active=1"
        sql += " ORDER BY rowid DESC"
        cur = await db.execute(sql)
        return [dict(row) for row in await cur.fetchall()]


async def create_experiment(*, offer_id: str, channel: str, variant: str,
                            experiment_id: str | None = None) -> dict:
    await init_db()
    experiment_id = experiment_id or str(uuid.uuid4())
    async with __import__("aiosqlite").connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO experiments
               (id,offer_id,channel,variant,started_at)
               VALUES (?,?,?,?,?)""",
            (experiment_id, offer_id, channel, variant, _now()),
        )
        await db.commit()
    return await get_experiment(experiment_id)


async def get_experiment(experiment_id: str) -> dict | None:
    await init_db()
    async with __import__("aiosqlite").connect(DB_PATH) as db:
        db.row_factory = __import__("aiosqlite").Row
        cur = await db.execute("SELECT * FROM experiments WHERE id=?", (experiment_id,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def list_experiments() -> list[dict]:
    await init_db()
    async with __import__("aiosqlite").connect(DB_PATH) as db:
        db.row_factory = __import__("aiosqlite").Row
        cur = await db.execute(
            "SELECT * FROM experiments ORDER BY started_at DESC"
        )
        return [dict(row) for row in await cur.fetchall()]


async def record_metrics(experiment_id: str, *, impressions: int = 0,
                         clicks: int = 0, conversions: int = 0,
                         revenue: float = 0.0, spend: float = 0.0) -> dict | None:
    values = [impressions, clicks, conversions]
    if any(int(v) < 0 for v in values) or float(revenue) < 0 or float(spend) < 0:
        raise ValueError("metrics must be non-negative")
    await init_db()
    async with __import__("aiosqlite").connect(DB_PATH) as db:
        await db.execute(
            """UPDATE experiments
               SET impressions=impressions+?,
                   clicks=clicks+?,
                   conversions=conversions+?,
                   revenue=revenue+?,
                   spend=spend+?
               WHERE id=?""",
            (int(impressions), int(clicks), int(conversions), float(revenue), float(spend), experiment_id),
        )
        await db.commit()
    return await get_experiment(experiment_id)


async def tracked_offer_url(offer_id: str, *, source: str, medium: str,
                            campaign: str, content: str | None = None) -> str | None:
    offer = await get_offer(offer_id)
    if not offer:
        return None
    return add_utm(
        offer["url"],
        source=source,
        medium=medium,
        campaign=campaign,
        content=content,
    )


async def learning_decision(experiment_id: str, sample_floor: int = 30) -> dict | None:
    experiment = await get_experiment(experiment_id)
    if not experiment:
        return None
    decision = LearningEngine().evaluate(
        clicks=experiment["clicks"],
        conversions=experiment["conversions"],
        revenue=experiment["revenue"],
        spend=experiment["spend"],
        sample_floor=sample_floor,
    )
    return {
        "experiment_id": experiment_id,
        "action": decision.action,
        "reason": decision.reason,
        "confidence": decision.confidence,
    }


async def analytics() -> dict:
    await init_db()
    async with __import__("aiosqlite").connect(DB_PATH) as db:
        cur = await db.execute(
            """SELECT
                 COALESCE(SUM(impressions),0),
                 COALESCE(SUM(clicks),0),
                 COALESCE(SUM(conversions),0),
                 COALESCE(SUM(revenue),0),
                 COALESCE(SUM(spend),0)
               FROM experiments"""
        )
        impressions, clicks, conversions, revenue, spend = await cur.fetchone()
    impressions, clicks, conversions = map(int, (impressions, clicks, conversions))
    revenue = float(revenue)
    spend = float(spend)
    ctr = clicks / impressions if impressions else 0.0
    cr = conversions / clicks if clicks else 0.0
    epc = revenue / clicks if clicks else 0.0
    return {
        "impressions": impressions,
        "clicks": clicks,
        "conversions": conversions,
        "revenue": round(revenue, 4),
        "spend": round(spend, 4),
        "profit": round(revenue - spend, 4),
        "ctr": round(ctr, 6),
        "conversion_rate": round(cr, 6),
        "epc": round(epc, 6),
        "source": "SQLite experiment data",
    }


async def import_observed_offers(rows: list[dict]) -> list[dict]:
    """Persist only observed feed fields; no invented performance metrics."""
    imported = []
    for row in rows:
        if not row.get("title") or not row.get("url") or not row.get("country"):
            continue
        imported.append(await create_offer(
            title=str(row["title"]), url=str(row["url"]),
            payout=float(row.get("payout") or 0), country=str(row["country"]),
            category=str(row.get("category") or "") or None,
            offer_id=str(row.get("id") or "") or None,
        ))
    return imported
