"""认证回归测试：public/private 模式、admin/viewer token 门禁。"""
import importlib
import os


def _make_client(monkeypatch, auth_mode="public", viewer="", admin=""):
    monkeypatch.setenv("DATA_SOURCE", "mock")
    monkeypatch.setenv("FEISHU_WORKTIME_SOURCE", "mock")
    monkeypatch.setenv("AUTH_MODE", auth_mode)
    monkeypatch.setenv("VIEWER_TOKEN", viewer)
    monkeypatch.setenv("ADMIN_TOKEN", admin)
    import app as app_mod
    importlib.reload(app_mod)
    app_mod.app.config.update(TESTING=True)
    return app_mod.app.test_client()


def test_public_mode_open(monkeypatch):
    c = _make_client(monkeypatch, "public")
    assert c.get("/api/tasks").status_code == 200
    assert c.get("/api/dashboard").status_code == 200


def test_private_no_token_401(monkeypatch):
    c = _make_client(monkeypatch, "private", viewer="v", admin="a")
    assert c.get("/api/tasks").status_code == 401
    assert c.get("/api/people").status_code == 401


def test_private_wrong_token_403(monkeypatch):
    c = _make_client(monkeypatch, "private", viewer="v", admin="a")
    r = c.get("/api/tasks", headers={"Authorization": "Bearer wrong"})
    assert r.status_code == 403


def test_private_viewer_token_ok(monkeypatch):
    c = _make_client(monkeypatch, "private", viewer="v", admin="a")
    r = c.get("/api/tasks", headers={"Authorization": "Bearer v"})
    assert r.status_code == 200


def test_private_admin_token_reads(monkeypatch):
    c = _make_client(monkeypatch, "private", viewer="v", admin="a")
    r = c.get("/api/people", headers={"Authorization": "Bearer a"})
    assert r.status_code == 200


def test_admin_sync_no_token_401(monkeypatch):
    c = _make_client(monkeypatch, "public", viewer="", admin="a")
    assert c.post("/api/admin/checkin/sync").status_code in (401, 503)


def test_admin_sync_wrong_token_401(monkeypatch):
    c = _make_client(monkeypatch, "public", viewer="", admin="a")
    r = c.post("/api/admin/checkin/sync", headers={"Authorization": "Bearer nope"})
    assert r.status_code == 401


def test_unknown_api_404(monkeypatch):
    c = _make_client(monkeypatch, "public")
    assert c.get("/api/does-not-exist").status_code == 404
