# tests/test_auth.py

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_register_and_login():
    """
    Testa o fluxo completo:
    - registra um novo usuário
    - faz login
    - usa o token pra chamar um endpoint protegido
    """
    # username "testuser_x" pra evitar conflito com admin
    username = "testuser_x"
    password = "senha123"

    # 1) registrar usuário
    resp_reg = client.post(
        "/api/auth/register",
        json={"username": username, "password": password},
    )
    assert resp_reg.status_code in (200, 201), resp_reg.text
    data_reg = resp_reg.json()
    assert data_reg["username"] == username

    # 2) fazer login
    resp_login = client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )
    assert resp_login.status_code == 200, resp_login.text
    data_login = resp_login.json()
    assert "access_token" in data_login
    token = data_login["access_token"]

    # 3) chamar um endpoint protegido (/api/content/strategy)
    payload = {
        "topic": "marketing digital",
        "platform": "instagram",
        "mode": "rich",
        "users": [],
    }

    resp_strategy = client.post(
        "/api/content/strategy",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_strategy.status_code == 200, resp_strategy.text
    data_strategy = resp_strategy.json()
    assert data_strategy["topic"] == payload["topic"]
    assert data_strategy["platform"] == payload["platform"]
