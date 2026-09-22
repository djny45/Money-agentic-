import pytest

from app.autopilot import list_autopilot_runs, run_autopilot


@pytest.mark.asyncio
async def test_autopilot_queues_only_selected_offers(tmp_path, monkeypatch):
    from app import autopilot, db, publish_store
    path = tmp_path / "autopilot.db"
    monkeypatch.setattr(db, "DB_PATH", path)
    monkeypatch.setattr(autopilot, "DB_PATH", path)
    monkeypatch.setattr(publish_store, "DB_PATH", path)

    await db.init_db()
    async with __import__("aiosqlite").connect(path) as conn:
        await conn.execute(
            "INSERT INTO offers (id,title,url,payout,country,active) VALUES (?,?,?,?,?,?)",
            ("1","Example","https://example.test",1.0,"IN",1),
        )
        await conn.commit()

    result = await run_autopilot(channel="postiz", limit=5)
    assert result["queued"] == 1
    assert (await list_autopilot_runs())[0]["status"] == "completed"
