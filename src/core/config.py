# src/core/config.py

import os
from pydantic import BaseModel


class Settings(BaseModel):
    # Chave secreta para assinar os tokens JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "change-me-in-production-super-secret-key",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h

    # (opcional) URL do banco – já está sendo tratada no sqlmodel_db via DB_PATH
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    class Config:
        arbitrary_types_allowed = True


settings = Settings()
