import pytest

from app.audit import list_audit, log_action


@pytest.mark.asyncio
async def test_audit_log_round_trip(tmp_path, monkeypatch):
    from app import audit, db

    path = tmp_path / "audit.db"
    monkeypatch.setattr(db, "DB_PATH", path)
    monkeypatch.setattr(audit, "DB_PATH", path)

    await log_action("test_action", actor="test", target="x", details={"ok": True})
    rows = await list_audit()

    assert rows[0]["action"] == "test_action"
    assert rows[0]["actor"] == "test"
