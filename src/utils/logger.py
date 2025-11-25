import logging


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger configurado para o projeto.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:  # evita duplicação de mensagens
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
