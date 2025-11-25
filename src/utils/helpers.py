def clean_text(text: str) -> str:
    """
    Remove espaços extras e padroniza texto.
    """
    return " ".join(text.strip().split())


def normalize_topic(topic: str) -> str:
    """
    Padroniza o tema para facilitar análise futura.
    """
    return topic.lower().strip()
