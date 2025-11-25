from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from src.audience_analyzer.audience_core import analyze_audience, profile_audience
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


# ----------------------------
# MODELOS DE ENTRADA
# ----------------------------


class AudienceUser(BaseModel):
    age: int
    gender: str
    region: str


class AudienceRequest(BaseModel):
    users: List[AudienceUser]


# ----------------------------
# ENDPOINT 1 — /audience/analyze
# ----------------------------


@router.post("/audience/analyze")
def analyze_audience_endpoint(payload: AudienceRequest):
    """
    Retorna análise simples do público.
    """
    logger.info(f"Analisando {len(payload.users)} usuários")

    users_dicts = [user.dict() for user in payload.users]
    result = analyze_audience(users_dicts)

    return {
        "summary": result,
        "input_size": len(payload.users),
    }


# ----------------------------
# ENDPOINT 2 — /audience/profile
# ----------------------------


@router.post("/audience/profile")
def audience_profile_endpoint(payload: AudienceRequest):
    """
    Gera perfis simplificados do público.
    """
    logger.info(f"Gerando perfil para {len(payload.users)} usuários")

    users_dicts = [user.dict() for user in payload.users]
    profiles = profile_audience(users_dicts)

    return {
        "total_users": len(payload.users),
        "profiles": profiles,
    }
