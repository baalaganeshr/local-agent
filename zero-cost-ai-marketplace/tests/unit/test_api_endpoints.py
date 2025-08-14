from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_chat_basic():
    payload = {"messages": [{"role": "user", "content": "Hello"}], "user_id": "u1", "tier": "basic"}
    r = client.post("/api/chat", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "content" in data and data["content"]
    assert data["tier"] == "basic"

def test_analytics():
    r = client.get("/api/analytics")
    assert r.status_code == 200
    body = r.json()
    assert "total_conversations" in body

def test_feedback():
    fb = {"conversation_id": 1, "rating": 5, "comment": "Great", "user_id": "u1"}
    r = client.post("/api/feedback", json=fb)
    assert r.status_code == 200
    assert r.json()["status"] == "received"
