import secrets
from typing import Dict

from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel

from src.database.db import get_user_by_username
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

# token -> username (apenas em memória, suficiente para dev)
active_tokens: Dict[str, str] = {}


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


@router.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    user = get_user_by_username(payload.username)

    if not user:
        logger.warning(
            f"Tentativa de login falhou: usuário {payload.username} não encontrado"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    # Aqui a senha está em texto puro no banco (para dev)
    if user["password"] != payload.password:
        logger.warning(
            f"Tentativa de login falhou: senha inválida para {payload.username}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    token = secrets.token_hex(32)
    active_tokens[token] = payload.username

    logger.info(f"Login bem-sucedido para usuário {payload.username}")

    return LoginResponse(access_token=token, username=payload.username)


def get_current_user(authorization: str = Header(None)):
    """
    Dependency para proteger endpoints.
    Espera header: Authorization: Bearer <token>
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não informado",
        )

    token = authorization.split(" ", 1)[1].strip()
    username = active_tokens.get(token)

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )

    return username
