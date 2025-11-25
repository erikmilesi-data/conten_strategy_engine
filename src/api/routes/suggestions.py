from fastapi import APIRouter, Query
from src.suggestion_engine.suggestion_core import get_basic_suggestions
from src.utils.logger import get_logger
from src.utils.helpers import normalize_topic

logger = get_logger(__name__)
router = APIRouter()


@router.get("/suggestions")
def generate_suggestions(
    topic: str = Query(..., description="Tema para gerar sugestões"),
):
    """
    Gera sugestões de posts com base em um tema.
    """
    topic = normalize_topic(topic)
    logger.info(f"Recebido pedido de sugestões para o tema: {topic}")

    suggestions = get_basic_suggestions(topic)

    return {
        "topic": topic,
        "total_suggestions": len(suggestions),
        "suggestions": suggestions,
    }
