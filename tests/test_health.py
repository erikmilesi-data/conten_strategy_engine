# tests/test_health.py

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_root_ok():
    """Verifica se o endpoint raiz está respondendo."""
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data
    assert "Content Strategy Engine" in data["message"]


def test_health_ok():
    """Se você tiver um /api/health, testa aqui."""
    resp = client.get("/api/health")
    # se não tiver esse endpoint ainda, pode comentar esse teste
    assert resp.status_code == 200
