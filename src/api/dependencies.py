"""
Dependencias de FastAPI para inyección de dependencias.
"""

from typing import Annotated
from fastapi import Depends
from ..database import get_database, Database
from ..repositories import TaskRepository
from ..services import TaskService


def get_task_repository(
    db: Annotated[Database, Depends(get_database)],
) -> TaskRepository:
    """
    Obtiene una instancia del repositorio de tareas.

    Args:
        db: Base de datos inyectada.

    Returns:
        Repositorio de tareas.
    """
    return TaskRepository(db)


def get_task_service(
    repository: Annotated[TaskRepository, Depends(get_task_repository)],
) -> TaskService:
    """
    Obtiene una instancia del servicio de tareas.

    Args:
        repository: Repositorio inyectado.

    Returns:
        Servicio de tareas.
    """
    return TaskService(repository)
