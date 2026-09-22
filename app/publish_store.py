from datetime import datetime, timezone
import aiosqlite

from .db import DB_PATH, init_db


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def enqueue(channel: str, text: str, url: str) -> dict:
    if not channel.strip() or not text.strip() or not url.strip():
        raise ValueError("channel, text and url are required")
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO publish_queue (channel,text,url,created_at) VALUES (?,?,?,?)",
            (channel, text, url, _now()),
        )
        await db.commit()
        item_id = cur.lastrowid
    return await get_item(item_id)


async def get_item(item_id: int) -> dict | None:
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM publish_queue WHERE id=?", (item_id,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def list_items(status: str | None = None) -> list[dict]:
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        if status:
            cur = await db.execute(
                "SELECT * FROM publish_queue WHERE status=? ORDER BY id DESC", (status,)
            )
        else:
            cur = await db.execute("SELECT * FROM publish_queue ORDER BY id DESC")
        return [dict(row) for row in await cur.fetchall()]


async def approve(item_id: int) -> dict | None:
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE publish_queue SET approved=1,status='approved',approved_at=? "
            "WHERE id=? AND status='pending'",
            (_now(), item_id),
        )
        await db.commit()
    return await get_item(item_id)
