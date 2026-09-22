import json
from datetime import datetime, timezone

import aiosqlite

from .db import DB_PATH, init_db
from .learning import LearningEngine
from .strategy import StrategyManager
from .strategy_store import get_strategy, save_strategy


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def optimize_experiments(*, sample_floor: int = 30) -> dict:
    """Evaluate experiments, update versioned strategies, and flag regressions."""
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT e.*, o.title AS offer_title FROM experiments e "
            "LEFT JOIN offers o ON o.id=e.offer_id ORDER BY e.started_at DESC"
        )
        experiments = await cur.fetchall()

    engine = LearningEngine()
    decisions = []
    promoted = revised = paused = regressions = 0

    for exp in experiments:
        decision = engine.evaluate(
            clicks=int(exp["clicks"]), conversions=int(exp["conversions"]),
            revenue=float(exp["revenue"]), spend=float(exp["spend"]),
            sample_floor=sample_floor,
        )
        key = f"{exp['channel']}:{(exp['offer_title'] or exp['offer_id'])[:40]}"
        strategy = await get_strategy(key)

        item = {
            "experiment_id": exp["id"], "offer_id": exp["offer_id"],
            "channel": exp["channel"], "variant": exp["variant"],
            "action": decision.action, "confidence": decision.confidence,
            "reason": decision.reason,
        }

        # A previously promoted strategy turning negative is a regression signal.
        if strategy and decision.action == "revise_strategy":
            evidence = json.loads(strategy["evidence_json"])
            if evidence.get("decision") == "retain_and_test":
                item["regression"] = True
                regressions += 1
            revised += 1
        elif decision.action == "retain_and_test":
            base = StrategyManager().propose(exp["offer_title"] or exp["offer_id"], exp["channel"])
            base.evidence.update({
                "latest_experiment": exp["id"],
                "decision": decision.action,
                "updated_at": _now(),
            })
            await save_strategy(base)
            promoted += 1
        elif decision.action == "pause_experiment":
            paused += 1
        elif decision.action == "revise_strategy":
            revised += 1

        decisions.append(item)

    return {
        "status": "completed", "sample_floor": sample_floor,
        "evaluated": len(decisions), "promoted": promoted,
        "revised": revised, "paused": paused, "regressions": regressions,
        "decisions": decisions,
    }
