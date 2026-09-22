import pytest

from app.publish_store import approve, enqueue, list_items


@pytest.mark.asyncio
async def test_publish_queue_requires_explicit_approval(tmp_path, monkeypatch):
    from app import db, publish_store
    path = tmp_path / "queue.db"
    monkeypatch.setattr(db, "DB_PATH", path)
    monkeypatch.setattr(publish_store, "DB_PATH", path)

    item = await enqueue("postiz", "draft", "https://example.test")
    assert item["status"] == "pending"
    approved = await approve(item["id"])
    assert approved["approved"] == 1
    assert approved["status"] == "approved"
    assert len(await list_items("approved")) == 1
