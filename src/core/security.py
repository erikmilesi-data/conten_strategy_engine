# src/core/security.py

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.config import settings

# ---------------------------
# Configuração básica de segurança
# ---------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Tenta pegar do settings; se não existir, usa defaults seguros
SECRET_KEY: str = getattr(settings, "SECRET_KEY", "change-me-in-prod")
ALGORITHM: str = getattr(settings, "ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 60)


# ---------------------------
# Funções de senha
# ---------------------------


def get_password_hash(password: str) -> str:
    """
    Gera hash seguro para senha.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara senha em texto puro com hash armazenado.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------
# Funções de JWT
# ---------------------------


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Cria um JWT a partir de um payload (data).
    Adiciona campo 'exp' automaticamente.
    """
    to_encode = data.copy()

    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decodifica o JWT e retorna o payload.
    Levanta JWTError se o token for inválido ou expirado.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload
    except JWTError as e:
        # Deixa o chamador (auth.py) decidir qual HTTPException levantar
        raise e
