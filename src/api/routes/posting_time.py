from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from src.posting_time_optimizer.time_core import suggest_best_times
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


class PostingTimeRequest(BaseModel):
    platform: str
    main_age_bucket: Optional[str] = None
    region_main: Optional[str] = None


@router.post("/posting/best-times")
def posting_best_times(payload: PostingTimeRequest):
    """
    Sugere melhores horários de postagem com base na plataforma
    e em informações simples do público.
    """
    logger.info(
        f"Requisição de melhores horários para plataforma={payload.platform}, "
        f"age_bucket={payload.main_age_bucket}, region={payload.region_main}"
    )

    result = suggest_best_times(
        platform=payload.platform,
        main_age_bucket=payload.main_age_bucket,
        region_main=payload.region_main,
    )

    return result
