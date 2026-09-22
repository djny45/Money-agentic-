import json
from datetime import datetime, timezone

import aiosqlite

from .db import DB_PATH, init_db


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def log_action(action: str, *, actor: str = "control-panel",
                     target: str | None = None, details: dict | None = None) -> None:
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO audit_log (action, actor, target, details_json, created_at) VALUES (?,?,?,?,?)",
            (action, actor, target, json.dumps(details or {}, sort_keys=True), _now()),
        )
        await db.commit()


async def list_audit(limit: int = 100) -> list[dict]:
    await init_db()
    limit = max(1, min(int(limit), 500))
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, action, actor, target, details_json, created_at "
            "FROM audit_log ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return [dict(row) for row in await cur.fetchall()]
