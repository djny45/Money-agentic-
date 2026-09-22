from datetime import datetime, timezone
import aiosqlite
from .db import DB_PATH

class StrategyMemory:
    async def remember(self, source: str, topic: str, content: str) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO knowledge(source, topic, content, created_at) VALUES (?, ?, ?, ?)",
                (source, topic, content, datetime.now(timezone.utc).isoformat()),
            )
            await db.commit()

    async def recent(self, topic: str, limit: int = 20) -> list[dict]:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute(
                "SELECT source, topic, content, created_at FROM knowledge "
                "WHERE topic = ? ORDER BY id DESC LIMIT ?", (topic, limit))
            return [dict(row) for row in await cur.fetchall()]
