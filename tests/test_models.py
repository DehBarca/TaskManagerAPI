"""
Pruebas unitarias para los modelos de datos.
"""

from datetime import datetime, timedelta

from pydantic import ValidationError
import pytest

from src.models import Task, TaskCreate, TaskPriority, TaskStatus, TaskUpdate


class TestTaskEnums:
    """Pruebas para las enumeraciones."""

    def test_task_status_values(self):
        """Verifica que los valores de TaskStatus sean correctos."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.CANCELLED.value == "cancelled"

    def test_task_priority_values(self):
        """Verifica que los valores de TaskPriority sean correctos."""
        assert TaskPriority.LOW.value == "low"
        assert TaskPriority.MEDIUM.value == "medium"
        assert TaskPriority.HIGH.value == "high"
        assert TaskPriority.URGENT.value == "urgent"


class TestTaskCreate:
    """Pruebas para el modelo TaskCreate."""

    def test_create_task_with_valid_data(self):
        """Prueba crear una tarea con datos válidos."""
        task_data = TaskCreate(
            title="Tarea de Prueba",
            description="Descripción",
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING,
            due_date=datetime.now() + timedelta(days=1),
        )
        assert task_data.title == "Tarea de Prueba"
        assert task_data.priority == TaskPriority.HIGH

    def test_create_task_with_minimal_data(self):
        """Prueba crear una tarea con datos mínimos."""
        task_data = TaskCreate(title="Tarea Mínima")
        assert task_data.title == "Tarea Mínima"
        assert task_data.priority == TaskPriority.MEDIUM  # Valor por defecto
        assert task_data.status == TaskStatus.PENDING  # Valor por defecto
        assert task_data.description is None

    def test_create_task_with_empty_title_fails(self):
        """Prueba que falla al crear una tarea con título vacío."""
        with pytest.raises(ValidationError):
            TaskCreate(title="   ")

    def test_create_task_with_past_due_date_fails(self):
        """Prueba que falla al crear una tarea con fecha pasada."""
        with pytest.raises(ValidationError):
            TaskCreate(title="Tarea", due_date=datetime.now() - timedelta(days=1))

    def test_create_task_title_strips_whitespace(self):
        """Prueba que el título se limpia de espacios."""
        task_data = TaskCreate(title="  Tarea con espacios  ")
        assert task_data.title == "Tarea con espacios"


class TestTaskUpdate:
    """Pruebas para el modelo TaskUpdate."""

    def test_update_task_with_partial_data(self):
        """Prueba actualizar solo algunos campos."""
        update_data = TaskUpdate(title="Nuevo Título")
        assert update_data.title == "Nuevo Título"
        assert update_data.description is None
        assert update_data.status is None

    def test_update_task_with_empty_title_fails(self):
        """Prueba que falla al actualizar con título vacío."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="   ")


class TestTask:
    """Pruebas para el modelo Task completo."""

    def test_create_full_task(self):
        """Prueba crear una tarea completa."""
        now = datetime.now()
        task = Task(
            id="test-id-123",
            title="Tarea Completa",
            description="Descripción completa",
            priority=TaskPriority.URGENT,
            status=TaskStatus.IN_PROGRESS,
            due_date=now + timedelta(days=5),
            created_at=now,
            updated_at=now,
        )
        assert task.id == "test-id-123"
        assert task.title == "Tarea Completa"
        assert task.priority == TaskPriority.URGENT
        assert task.status == TaskStatus.IN_PROGRESS

    def test_task_model_dump(self):
        """Prueba la serialización del modelo."""
        now = datetime.now()
        task = Task(id="test-id", title="Tarea", created_at=now, updated_at=now)
        task_dict = task.model_dump()
        assert isinstance(task_dict, dict)
        assert task_dict["id"] == "test-id"
        assert task_dict["title"] == "Tarea"
