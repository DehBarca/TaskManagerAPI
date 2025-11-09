"""
Configuración del sistema de logging.
"""

import logging
import sys
from typing import Optional
from ..config import settings


def setup_logging():
    """Configura el sistema de logging de la aplicación."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level, format=log_format, handlers=[logging.StreamHandler(sys.stdout)]
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Obtiene un logger configurado.

    Args:
        name: Nombre del logger. Si es None, usa el nombre del módulo llamante.

    Returns:
        Logger configurado.
    """
    if name is None:
        name = __name__

    logger = logging.getLogger(name)
    return logger
