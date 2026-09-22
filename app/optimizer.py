import json
from datetime import datetime, timezone

import aiosqlite

from .db import DB_PATH, init_db
from .learning import LearningEngine
from .strategy import StrategyManager
from .strategy_store import get_strategy, save_strategy, rollback_strategy


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def optimize_experiments(*, sample_floor: int = 30) -> dict:
    """Evaluate completed experiments and persist strategy improvements.

    Optimization changes strategy state only; it never rewrites executable code
    and never publishes content. Negative-profit strategies are not promoted.
    """
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM experiments ORDER BY started_at DESC"
        )
        experiments = await cur.fetchall()

    engine = LearningEngine()
    decisions = []
    promoted = 0
    revised = 0
    paused = 0

    for exp in experiments:
        decision = engine.evaluate(
            clicks=int(exp["clicks"]),
            conversions=int(exp["conversions"]),
            revenue=float(exp["revenue"]),
            spend=float(exp["spend"]),
            sample_floor=sample_floor,
        )
        item = {
            "experiment_id": exp["id"],
            "offer_id": exp["offer_id"],
            "channel": exp["channel"],
            "variant": exp["variant"],
            "action": decision.action,
            "confidence": decision.confidence,
            "reason": decision.reason,
        }
        decisions.append(item)

        if decision.action == "retain_and_test":
            strategy = await get_strategy(f"{exp['channel']}:{exp['offer_id'][:40]}")
            base = StrategyManager().propose(exp["offer_id"], exp["channel"])
            if strategy:
                base.evidence = {
                    **json.loads(strategy["evidence_json"]),
                    "latest_experiment": exp["id"],
                    "decision": decision.action,
                    "updated_at": _now(),
                }
            else:
                base.evidence.update({
                    "latest_experiment": exp["id"],
                    "decision": decision.action,
                    "updated_at": _now(),
                })
            await save_strategy(base)
            promoted += 1
        elif decision.action == "revise_strategy":
            revised += 1
        elif decision.action == "pause_experiment":
            paused += 1

    return {
        "status": "completed",
        "sample_floor": sample_floor,
        "evaluated": len(decisions),
        "promoted": promoted,
        "revised": revised,
        "paused": paused,
        "decisions": decisions,
    }
