from collections import Counter
from typing import List, Dict, Any


def _age_bucket(age: int) -> str:
    """
    Converte idade para faixa etária aproximada.
    """
    if age < 18:
        return "menos de 18"
    elif age < 25:
        return "18-24"
    elif age < 35:
        return "25-34"
    elif age < 45:
        return "35-44"
    elif age < 60:
        return "45-59"
    else:
        return "60+"


def analyze_audience(users: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Recebe uma lista de usuários (idade, gênero, região) e
    retorna um resumo estatístico simples.
    """
    genders = []
    regions = []
    age_buckets = []

    for user in users:
        age = user.get("age")
        gender = user.get("gender", "unknown")
        region = user.get("region", "unknown")

        if isinstance(age, int):
            age_buckets.append(_age_bucket(age))

        genders.append(gender)
        regions.append(region)

    gender_counts = Counter(genders)
    region_counts = Counter(regions)
    age_bucket_counts = Counter(age_buckets)

    return {
        "total_users": len(users),
        "by_gender": dict(gender_counts),
        "by_region": dict(region_counts),
        "by_age_bucket": dict(age_bucket_counts),
    }


def profile_audience(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Cria perfis simplificados de público com base na idade.
    """
    if not users:
        return []

    age_buckets = []

    for user in users:
        age = user.get("age")
        if isinstance(age, int):
            age_buckets.append(_age_bucket(age))

    total = len(age_buckets)
    if total == 0:
        return []

    counts = Counter(age_buckets)

    profiles = []
    for bucket, count in counts.items():
        percent = round((count / total) * 100, 1)

        if bucket in ("menos de 18", "18-24"):
            label = "iniciante"
        elif bucket in ("25-34", "35-44"):
            label = "intermediário"
        else:
            label = "avançado"

        profiles.append({"age_bucket": bucket, "type": label, "percent": percent})

    profiles.sort(key=lambda x: x["percent"], reverse=True)

    return profiles
