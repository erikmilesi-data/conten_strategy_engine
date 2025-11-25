from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)


@dataclass
class AppSettings:
    """
    Configurações principais do aplicativo.
    No futuro, podemos expandir para API keys, banco de dados, etc.
    """

    app_name: str = "Content Strategy Engine"
    environment: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("APP_DEBUG", "true").lower() == "true"


settings = AppSettings()
