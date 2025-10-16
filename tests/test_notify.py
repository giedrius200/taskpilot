from fastapi.testclient import TestClient


def test_background_notify(tmp_path, monkeypatch):
    # use an isolated sqlite DB for this test
    from src import db
    db_url = f"sqlite:///{tmp_path / 'notify.db'}"
    monkeypatch.setattr("src.db.DATABASE_URL", db_url)
    from sqlmodel import create_engine
    db.engine = create_engine(db_url, connect_args={"check_same_thread": False})
    # import models so SQLModel metadata contains table definitions before create_all
    import src.models  # noqa: F401
    db.init_db()

    # capture calls to notify_user
    called = []

    def fake_notify(task_id: int):
        called.append(task_id)

    monkeypatch.setattr("src.app.notify_user", fake_notify)

    from src.app import app

    client = TestClient(app)

    # register and login
    r = client.post("/register", json={"username": "alice", "password": "secret"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # create a task - this should schedule and run the background notify
    r2 = client.post("/tasks", json={"title": "Notify me", "description": "test"}, headers=headers)
    assert r2.status_code == 200

    # TestClient runs background tasks synchronously after the response, so our fake_notify should have been called
    assert called, "notify_user was not called"
    assert isinstance(called[0], int)
