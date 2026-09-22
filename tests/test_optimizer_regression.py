import pytest
from app.optimizer import optimize_experiments

@pytest.mark.asyncio
async def test_optimizer_flags_regression(tmp_path, monkeypatch):
    from app import db, optimizer, strategy_store
    from app.models import Strategy
    path = tmp_path / "regression.db"
    monkeypatch.setattr(db, "DB_PATH", path)
    monkeypatch.setattr(optimizer, "DB_PATH", path)
    monkeypatch.setattr(strategy_store, "DB_PATH", path)
    await db.init_db()
    await strategy_store.save_strategy(
        Strategy("social:Offer One", "h", ["a"], {"decision": "retain_and_test"})
    )
    async with __import__("aiosqlite").connect(path) as conn:
        await conn.execute(
            "INSERT INTO experiments "
            "(id,offer_id,channel,variant,impressions,clicks,conversions,revenue,spend,started_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            ("e1","offer1","social","v2",100,40,2,2.0,10.0,"2026-01-01T00:00:00+00:00"),
        )
        await conn.execute(
            "INSERT INTO offers (id,title,url,payout,country,active) "
            "VALUES (?,?,?,?,?,?)",
            ("offer1","Offer One","https://example.test",1.0,"IN",1),
        )
        await conn.commit()
    result = await optimize_experiments(sample_floor=30)
    assert result["regressions"] == 1
