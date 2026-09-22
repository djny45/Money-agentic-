from pathlib import Path
import aiosqlite

DB_PATH = Path("data/money_agentic.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS offers (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  payout REAL NOT NULL,
  country TEXT NOT NULL,
  category TEXT,
  conversion_rate REAL,
  epc REAL,
  active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS experiments (
  id TEXT PRIMARY KEY,
  offer_id TEXT NOT NULL,
  channel TEXT NOT NULL,
  variant TEXT NOT NULL,
  impressions INTEGER DEFAULT 0,
  clicks INTEGER DEFAULT 0,
  conversions INTEGER DEFAULT 0,
  revenue REAL DEFAULT 0,
  spend REAL DEFAULT 0,
  started_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS strategies (
  name TEXT PRIMARY KEY,
  version INTEGER NOT NULL,
  hypothesis TEXT NOT NULL,
  actions_json TEXT NOT NULL,
  evidence_json TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS knowledge (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  topic TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TEXT NOT NULL
);
"""

async def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()
