from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.suggestion_engine.suggestion_core import (
    get_basic_suggestions,
    get_platform_suggestions,
)
from src.audience_analyzer.audience_core import (
    analyze_audience,
    profile_audience,
)
from src.posting_time_optimizer.time_core import suggest_best_times
from src.utils.logger import get_logger
from src.database.db import save_analysis, list_history, load_entry
from src.api.routes.auth import get_current_user  # ✅ apenas a função

import json

logger = get_logger(__name__)
router = APIRouter()


class AudienceUser(BaseModel):
    age: int
    gender: str
    region: str


class ContentStrategyRequest(BaseModel):
    topic: str
    platform: str
    mode: str = "rich"
    users: Optional[List[AudienceUser]] = []


@router.post("/strategy")
def generate_content_strategy(
    request: ContentStrategyRequest,
    current_user: dict = Depends(get_current_user),  # ✅ trata como dict
):
    """
    Gera a estratégia completa e salva no histórico,
    associando ao usuário autenticado.
    """
    logger.info(
        f"[user={current_user.get('username')}] Gerando estratégia para topic={request.topic}, "
        f"platform={request.platform}, users={len(request.users or [])}"
    )

    # Converte Pydantic -> dict
    users_dicts = [u.dict() for u in (request.users or [])]

    # --- Análise de público ---
    audience_summary = analyze_audience(users_dicts)
    audience_profiles = profile_audience(users_dicts)

    dominant_profile = audience_profiles[0] if audience_profiles else None
    dominant_age_bucket = dominant_profile["age_bucket"] if dominant_profile else None
    dominant_region = (
        max(audience_summary["by_region"], key=audience_summary["by_region"].get)
        if audience_summary.get("by_region")
        else None
    )

    # --- Sugestões de conteúdo ---
    if request.mode == "basic":
        suggestions = get_basic_suggestions(request.topic)
    else:
        suggestions = get_platform_suggestions(request.topic, request.platform)

    # --- Horários ---
    time_slots = suggest_best_times(
        platform=request.platform,
        main_age_bucket=dominant_age_bucket,
        region_main=dominant_region,
    )

    final_response = {
        "topic": request.topic,
        "platform": request.platform,
        "mode": request.mode,
        "audience": {
            "summary": audience_summary,
            "profiles": audience_profiles,
            "dominant_profile": dominant_profile,
        },
        "suggestions": suggestions,
        "best_times": time_slots,
    }

    # 💾 Salvar no histórico vinculado ao usuário logado
    save_analysis(
        topic=request.topic,
        platform=request.platform,
        mode=request.mode,
        users=users_dicts,
        result=final_response,
        owner_username=current_user.get("username"),  # ✅ usa dict
    )

    return final_response


@router.get("/history")
def get_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
):
    """
    Retorna o histórico SOMENTE do usuário logado.
    """
    rows = list_history(limit=limit, owner_username=current_user.get("username"))
    return {"history": [dict(r) for r in rows]}


@router.get("/history/{entry_id}")
def get_history_entry(
    entry_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Retorna uma entrada específica do histórico,
    garantindo que pertence ao usuário logado.
    """
    entry = load_entry(entry_id=entry_id, owner_username=current_user.get("username"))

    if not entry:
        return {"error": "Entry not found"}

    return {
        "id": entry["id"],
        "timestamp": entry["timestamp"],
        "topic": entry["topic"],
        "platform": entry["platform"],
        "mode": entry["mode"],
        "users": json.loads(entry["users_json"]),
        "result": json.loads(entry["result_json"]),
    }
