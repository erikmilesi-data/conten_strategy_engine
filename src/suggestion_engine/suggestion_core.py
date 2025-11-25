from src.utils.helpers import normalize_topic
from src.utils.logger import get_logger

logger = get_logger(__name__)


def get_basic_suggestions(topic: str):
    """
    Sugestões básicas simples.
    """
    topic = normalize_topic(topic)
    logger.info(f"Gerando sugestões básicas para: {topic}")

    return [
        f"Ideia 1 sobre {topic}",
        f"Ideia 2 sobre {topic}",
        f"Ideia 3 sobre {topic}",
    ]


def get_platform_suggestions(topic: str, platform: str):
    """
    Sugestões mais ricas, adaptadas por plataforma.
    """
    topic = normalize_topic(topic)
    platform = platform.lower()
    logger.info(f"Gerando sugestões ricas para '{topic}' em '{platform}'")

    suggestions = []

    if platform == "instagram":
        suggestions.extend(
            [
                {
                    "format": "reels",
                    "idea": f"Reels: '3 erros que te impedem de evoluir em {topic}'.",
                },
                {
                    "format": "carrossel",
                    "idea": f"Carrossel: '5 passos para melhorar seu {topic}'.",
                },
                {
                    "format": "story",
                    "idea": f"Story: Pergunte 'Qual sua maior dúvida sobre {topic}?'",
                },
            ]
        )

    elif platform == "tiktok":
        suggestions.extend(
            [
                {
                    "format": "short-video",
                    "idea": f"Vídeo curto: 'Ninguém te conta isso sobre {topic}...'",
                },
                {
                    "format": "duet",
                    "idea": f"Dueto reagindo a um vídeo polêmico sobre {topic}.",
                },
                {
                    "format": "trend",
                    "idea": f"Use uma trend para explicar um conceito de {topic}.",
                },
            ]
        )

    elif platform == "linkedin":
        suggestions.extend(
            [
                {
                    "format": "texto",
                    "idea": f"Post textual: explique um case real envolvendo {topic}.",
                },
                {
                    "format": "artigo",
                    "idea": f"Artigo: 'Panorama atual de {topic} e as próximas tendências'.",
                },
                {
                    "format": "carrossel",
                    "idea": f"Carrossel com dados e insights profissionais sobre {topic}.",
                },
            ]
        )

    else:
        suggestions.extend(
            [
                {
                    "format": "genérico",
                    "idea": f"Post introdutório com o básico de {topic}.",
                },
                {
                    "format": "genérico",
                    "idea": f"Lista: '5 mitos e verdades sobre {topic}'.",
                },
            ]
        )

    return {
        "topic": topic,
        "platform": platform,
        "suggestions": suggestions,
    }
