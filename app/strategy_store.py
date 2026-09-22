import json
from dataclasses import asdict
from datetime import datetime, timezone

import aiosqlite

from .db import DB_PATH, init_db
from .models import Strategy


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def save_strategy(strategy: Strategy) -> dict:
    """Persist a strategy as an immutable version and update the active pointer."""
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT COALESCE(MAX(version), 0) FROM strategy_versions WHERE name=?",
            (strategy.name,),
        )
        next_version = int((await cur.fetchone())[0]) + 1
        strategy.version = next_version
        await db.execute(
            "INSERT INTO strategy_versions "
            "(name,version,hypothesis,actions_json,evidence_json,updated_at) VALUES (?,?,?,?,?,?)",
            (strategy.name, next_version, strategy.hypothesis,
             json.dumps(strategy.actions), json.dumps(strategy.evidence), _now()),
        )
        await db.execute(
            "INSERT INTO strategies (name,version,hypothesis,actions_json,evidence_json,updated_at) "
            "VALUES (?,?,?,?,?,?) "
            "ON CONFLICT(name) DO UPDATE SET version=excluded.version,"
            "hypothesis=excluded.hypothesis,actions_json=excluded.actions_json,"
            "evidence_json=excluded.evidence_json,updated_at=excluded.updated_at",
            (strategy.name, next_version, strategy.hypothesis,
             json.dumps(strategy.actions), json.dumps(strategy.evidence), _now()),
        )
        await db.commit()
    return asdict(strategy)


async def get_strategy(name: str) -> dict | None:
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM strategies WHERE name=?", (name,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def list_strategy_versions(name: str) -> list[dict]:
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM strategy_versions WHERE name=? ORDER BY version DESC",
            (name,),
        )
        return [dict(row) for row in await cur.fetchall()]


async def rollback_strategy(name: str, version: int) -> dict | None:
    """Restore a previous version by creating a new active version from it."""
    versions = await list_strategy_versions(name)
    source = next((v for v in versions if int(v["version"]) == int(version)), None)
    if source is None:
        return None
    strategy = Strategy(
        name=name,
        hypothesis=source["hypothesis"],
        actions=json.loads(source["actions_json"]),
        evidence=json.loads(source["evidence_json"]),
    )
    return await save_strategy(strategy)
