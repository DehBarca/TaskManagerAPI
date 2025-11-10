"""
Configuración de pytest y fixtures compartidos.
"""

from datetime import datetime, timedelta

import pytest

from src.database import Database
from src.models import Task, TaskCreate, TaskPriority, TaskStatus
from src.repositories import TaskRepository
from src.services import TaskService


@pytest.fixture
def mock_database():
    """Fixture que proporciona una base de datos en memoria limpia."""
    db = Database()
    db.data = {"tasks": {}}
    return db


@pytest.fixture
def task_repository(mock_database):
    """Fixture que proporciona un repositorio de tareas."""
    return TaskRepository(mock_database)


@pytest.fixture
def task_service(task_repository):
    """Fixture que proporciona un servicio de tareas."""
    return TaskService(task_repository)


@pytest.fixture
def sample_task_data():
    """Fixture que proporciona datos de ejemplo para una tarea."""
    return TaskCreate(
        title="Tarea de Prueba",
        description="Esta es una descripción de prueba",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PENDING,
        due_date=datetime.now() + timedelta(days=7),
    )


@pytest.fixture
def sample_task(task_repository, sample_task_data):
    """Fixture que proporciona una tarea guardada en el repositorio."""
    task = Task(
        id="test-task-id-123",
        **sample_task_data.model_dump(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    return task_repository.save(task)
