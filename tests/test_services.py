import pytest
from app import services


@pytest.mark.asyncio
async def test_offer_and_experiment_metrics(tmp_path, monkeypatch):
    path = tmp_path / "test.db"
    from app import db
    monkeypatch.setattr(db, "DB_PATH", path)
    monkeypatch.setattr(services, "DB_PATH", path)
    await services.init_db()
    offer = await services.create_offer(
        title="Test offer", url="https://example.test", payout=1.5, country="IN"
    )
    exp = await services.create_experiment(
        offer_id=offer["id"], channel="test", variant="A"
    )
    await services.record_metrics(exp["id"], impressions=100, clicks=10, conversions=2, revenue=3, spend=1)
    metrics = await services.analytics()
    assert metrics["clicks"] == 10
    assert metrics["conversions"] == 2
    assert metrics["revenue"] == 3
    assert metrics["spend"] == 1
    assert metrics["profit"] == 2
    assert metrics["ctr"] == 0.1
    assert metrics["conversion_rate"] == 0.2
    assert metrics["epc"] == 0.3
