import pytest

from app.models import Strategy
from app.strategy_store import get_strategy, list_strategy_versions, rollback_strategy, save_strategy


@pytest.mark.asyncio
async def test_strategy_versions_and_rollback(tmp_path, monkeypatch):
    from app import db, strategy_store
    path = tmp_path / "strategy.db"
    monkeypatch.setattr(db, "DB_PATH", path)
    monkeypatch.setattr(strategy_store, "DB_PATH", path)

    first = await save_strategy(Strategy("social:offer", "h1", ["a"], {"x": 1}))
    second = await save_strategy(Strategy("social:offer", "h2", ["b"], {"x": 2}))
    assert first["version"] == 1
    assert second["version"] == 2

    active = await get_strategy("social:offer")
    assert active["version"] == 2

    restored = await rollback_strategy("social:offer", 1)
    assert restored["version"] == 3
    assert restored["hypothesis"] == "h1"
    assert len(await list_strategy_versions("social:offer")) == 3
