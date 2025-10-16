from fastapi.testclient import TestClient
from src.app import app


def test_duplicate_register(tmp_path, monkeypatch):
    # ensure isolated DB
    from src import db
    db_url = f"sqlite:///{tmp_path / 'test2.db'}"
    monkeypatch.setattr("src.db.DATABASE_URL", db_url)
    from sqlmodel import create_engine
    db.engine = create_engine(db_url, connect_args={"check_same_thread": False})
    db.init_db()

    client = TestClient(app)
    r = client.post("/register", json={"username": "bob", "password": "pw"})
    assert r.status_code == 200
    r2 = client.post("/register", json={"username": "bob", "password": "pw"})
    assert r2.status_code == 400


def test_invalid_token():
    client = TestClient(app)
    headers = {"Authorization": "Bearer invalid.token.here"}
    r = client.get("/tasks", headers=headers)
    assert r.status_code == 401
