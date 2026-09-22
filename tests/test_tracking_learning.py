import pytest
from app import services


@pytest.mark.asyncio
async def test_tracking_and_learning(tmp_path, monkeypatch):
    monkeypatch.setattr(services, "DB_PATH", tmp_path / "test.db")
    await services.init_db()
    offer = await services.create_offer(
        title="Tracked offer", url="https://example.test/path?x=1",
        payout=2.0, country="IN"
    )
    url = await services.tracked_offer_url(
        offer["id"], source="social", medium="organic",
        campaign="test", content="a"
    )
    assert "utm_source=social" in url
    assert "utm_campaign=test" in url
    exp = await services.create_experiment(
        offer_id=offer["id"], channel="social", variant="A"
    )
    decision = await services.learning_decision(exp["id"], sample_floor=30)
    assert decision["action"] == "collect_more_data"
