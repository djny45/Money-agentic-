import json
from datetime import datetime, timezone

import aiosqlite

from .compliance import ComplianceAgent
from .db import DB_PATH, init_db
from .models import Offer
from .offer_intelligence import OfferIntelligence
from .publish_store import enqueue


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def run_autopilot(*, channel: str, limit: int = 5) -> dict:
    """Run one bounded autopilot cycle.

    It selects only active offers with observed facts, creates transparent
    drafts, applies compliance gates, and queues drafts for explicit approval.
    It never publishes or creates artificial traffic.
    """
    await init_db()
    limit = max(1, min(int(limit), 20))
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM offers WHERE active=1 ORDER BY rowid DESC LIMIT ?",
            (limit,),
        )
        rows = await cur.fetchall()

    intelligence = OfferIntelligence()
    compliance = ComplianceAgent()
    selected = blocked = queued = 0
    details = []

    for row in rows:
        offer = Offer(
            id=row["id"], title=row["title"], url=row["url"],
            payout=row["payout"], country=row["country"],
            category=row["category"] or "",
            conversion_rate=row["conversion_rate"],
            epc=row["epc"], active=bool(row["active"]),
        )
        score = intelligence.score(offer)
        if score.score <= 0:
            blocked += 1
            details.append({"offer_id": offer.id, "status": "blocked", "reason": "no_positive_observed_score"})
            continue

        selected += 1
        result = compliance.check(authorized=True)
        if not result.allowed:
            blocked += 1
            details.append({"offer_id": offer.id, "status": "blocked", "reasons": result.reasons})
            continue

        text = (
            f"{offer.title}. Review the current offer details before deciding: "
            f"{offer.url}"
        )
        item = await enqueue(channel, text, offer.url)
        queued += 1
        details.append({
            "offer_id": offer.id,
            "status": "queued",
            "queue_id": item["id"],
            "score": score.score,
        })

    summary = {
        "channel": channel,
        "scanned": len(rows),
        "selected": selected,
        "queued": queued,
        "blocked": blocked,
        "details": details,
    }
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO automation_runs "
            "(mode,status,scanned,selected,queued,blocked,summary_json,created_at) "
            "VALUES (?,?,?,?,?,?,?,?)",
            ("bounded_autopilot", "completed", len(rows), selected, queued, blocked,
             json.dumps(summary, sort_keys=True), _now()),
        )
        await db.commit()
        run_id = cur.lastrowid

    return {"run_id": run_id, **summary}


async def list_autopilot_runs(limit: int = 20) -> list[dict]:
    await init_db()
    limit = max(1, min(int(limit), 100))
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM automation_runs ORDER BY id DESC LIMIT ?", (limit,)
        )
        return [dict(row) for row in await cur.fetchall()]
