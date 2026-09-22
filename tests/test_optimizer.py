import pytest

from app.models import Strategy
from app.optimizer import optimize_experiments


@pytest.mark.asyncio
async def test_optimizer_promotes_only_positive_measured_experiment(tmp_path, monkeypatch):
    from app import db, optimizer, strategy_store
    path = tmp_path / "optimizer.db"
    monkeypatch.setattr(db, "DB_PATH", path)
    monkeypatch.setattr(optimizer, "DB_PATH", path)
    monkeypatch.setattr(strategy_store, "DB_PATH", path)

    await db.init_db()
    async with __import__("aiosqlite").connect(path) as dbx:
        await dbx.execute(
            "INSERT INTO experiments "
            "(id,offer_id,channel,variant,impressions,clicks,conversions,revenue,spend,started_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            ("e1","offer1","postiz","v1",100,40,4,20.0,5.0,"2026-01-01T00:00:00+00:00"),
        )
        await dbx.commit()

    result = await optimize_experiments(sample_floor=30)
    assert result["promoted"] == 1
    assert result["evaluated"] == 1
