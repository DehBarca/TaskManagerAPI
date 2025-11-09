"""
Configuración de la aplicación.
Carga las variables de entorno y proporciona acceso a la configuración.
"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Configuración de la aplicación."""

    # Información de la aplicación
    APP_NAME: str = os.getenv("APP_NAME", "TaskManager")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_PREFIX: str = "/api/v1"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def get_database_path(cls) -> Optional[Path]:
        """Obtiene la ruta del archivo de base de datos SQLite."""
        if cls.DATABASE_URL.startswith("sqlite:///"):
            db_path = cls.DATABASE_URL.replace("sqlite:///", "")
            return Path(db_path)
        return None


# Instancia global de configuración
settings = Settings()
