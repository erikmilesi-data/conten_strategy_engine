from typing import Dict, List, Any


def _base_slots_for_platform(platform: str) -> List[str]:
    """
    Define janelas de horário base por plataforma (heurísticas simples).
    """
    platform = platform.lower()

    if platform == "instagram":
        # Manhã, fim de tarde e noite
        return ["07:00-09:00", "12:00-14:00", "18:00-21:00"]
    elif platform == "tiktok":
        # Mais forte à noite
        return ["12:00-14:00", "18:00-23:00"]
    elif platform == "linkedin":
        # Horário comercial
        return ["08:00-10:00", "12:00-13:00", "17:00-19:00"]
    else:
        # Genérico
        return ["09:00-11:00", "18:00-21:00"]


def suggest_best_times(
    platform: str,
    main_age_bucket: str | None = None,
    region_main: str | None = None,
) -> Dict[str, Any]:
    """
    Sugere melhores horários com base na plataforma e em informações simples do público.
    Por enquanto usa regras heurísticas, depois podemos sofisticar com dados reais.
    """
    slots = _base_slots_for_platform(platform)
    reasons: list[str] = []

    platform_lower = platform.lower()

    if platform_lower == "instagram":
        reasons.append(
            "Instagram tende a performar bem em horários em que as pessoas estão "
            "acordando, em pausa (almoço) e no pós-expediente."
        )
    elif platform_lower == "tiktok":
        reasons.append(
            "TikTok costuma ter pico de uso no fim da tarde e à noite, "
            "quando o público está relaxando."
        )
    elif platform_lower == "linkedin":
        reasons.append(
            "LinkedIn é mais forte em horário comercial, com destaque para começo "
            "da manhã e final do expediente."
        )
    else:
        reasons.append(
            "Como a plataforma não é reconhecida especificamente, foi aplicada "
            "uma janela genérica de horários com boa probabilidade de engajamento."
        )

    if main_age_bucket:
        reasons.append(
            f"Faixa etária predominante: {main_age_bucket}. "
            "Faixas 18-34 tendem a ser mais ativas à noite; faixas mais altas podem "
            "concentrar mais consumo em horários de pausa e início da noite."
        )

    if region_main:
        reasons.append(
            f"Região predominante: {region_main}. Os horários sugeridos consideram o "
            "fuso horário local; em um cenário real, os horários seriam ajustados "
            "por time zone e hábitos regionais."
        )

    return {
        "platform": platform_lower,
        "recommended_slots": slots,
        "notes": reasons,
    }
