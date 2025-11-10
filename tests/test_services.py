"""
Pruebas unitarias para los servicios.
"""

from datetime import datetime, timedelta

import pytest

from src.models import TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from src.utils.exceptions import (
    DuplicateTaskException,
    TaskNotFoundException,
)


class TestTaskService:
    """Pruebas para TaskService."""

    def test_get_all_tasks_empty(self, task_service):
        """Prueba obtener todas las tareas cuando no hay ninguna."""
        tasks = task_service.get_all_tasks()
        assert len(tasks) == 0

    def test_create_task(self, task_service, sample_task_data):
        """Prueba crear una nueva tarea."""
        task = task_service.create_task(sample_task_data)
        assert task.id is not None
        assert task.title == sample_task_data.title
        assert task.created_at is not None

    def test_create_task_with_past_due_date_fails(self, task_service):
        """Prueba que falla al crear una tarea con fecha pasada."""
        # La validación ocurre en Pydantic, no en el servicio
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            TaskCreate(title="Tarea", due_date=datetime.now() - timedelta(days=1))

    def test_create_duplicate_task_fails(self, task_service, sample_task_data):
        """Prueba que falla al crear una tarea duplicada."""
        task_service.create_task(sample_task_data)

        with pytest.raises(DuplicateTaskException):
            task_service.create_task(sample_task_data)

    def test_get_task_by_id(self, task_service, sample_task_data):
        """Prueba obtener una tarea por ID."""
        created_task = task_service.create_task(sample_task_data)

        found_task = task_service.get_task_by_id(created_task.id)
        assert found_task.id == created_task.id
        assert found_task.title == created_task.title

    def test_get_task_by_id_not_found(self, task_service):
        """Prueba que lanza excepción al buscar tarea inexistente."""
        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id("non-existent-id")

    def test_get_tasks_by_status(self, task_service):
        """Prueba filtrar tareas por estado."""
        # Crear tareas con diferentes estados
        task1_data = TaskCreate(title="Tarea 1", status=TaskStatus.PENDING)
        task2_data = TaskCreate(title="Tarea 2", status=TaskStatus.COMPLETED)
        task3_data = TaskCreate(title="Tarea 3", status=TaskStatus.PENDING)

        task_service.create_task(task1_data)
        task_service.create_task(task2_data)
        task_service.create_task(task3_data)

        pending_tasks = task_service.get_tasks_by_status(TaskStatus.PENDING)
        assert len(pending_tasks) == 2

    def test_update_task(self, task_service, sample_task_data):
        """Prueba actualizar una tarea."""
        created_task = task_service.create_task(sample_task_data)

        update_data = TaskUpdate(title="Título Actualizado", status=TaskStatus.IN_PROGRESS)
        updated_task = task_service.update_task(created_task.id, update_data)

        assert updated_task.title == "Título Actualizado"
        assert updated_task.status == TaskStatus.IN_PROGRESS

    def test_update_task_not_found(self, task_service):
        """Prueba actualizar una tarea que no existe."""
        update_data = TaskUpdate(title="Nuevo Título")

        with pytest.raises(TaskNotFoundException):
            task_service.update_task("non-existent-id", update_data)

    def test_update_task_duplicate_title_fails(self, task_service):
        """Prueba que falla al actualizar con un título duplicado."""
        task1_data = TaskCreate(title="Tarea 1")
        task2_data = TaskCreate(title="Tarea 2")

        task_service.create_task(task1_data)
        task2 = task_service.create_task(task2_data)

        update_data = TaskUpdate(title="Tarea 1")

        with pytest.raises(DuplicateTaskException):
            task_service.update_task(task2.id, update_data)

    def test_delete_task(self, task_service, sample_task_data):
        """Prueba eliminar una tarea."""
        created_task = task_service.create_task(sample_task_data)

        result = task_service.delete_task(created_task.id)
        assert result is True

        with pytest.raises(TaskNotFoundException):
            task_service.get_task_by_id(created_task.id)

    def test_delete_task_not_found(self, task_service):
        """Prueba eliminar una tarea que no existe."""
        with pytest.raises(TaskNotFoundException):
            task_service.delete_task("non-existent-id")

    def test_complete_task(self, task_service, sample_task_data):
        """Prueba marcar una tarea como completada."""
        created_task = task_service.create_task(sample_task_data)

        completed_task = task_service.complete_task(created_task.id)
        assert completed_task.status == TaskStatus.COMPLETED

    def test_get_statistics(self, task_service):
        """Prueba obtener estadísticas de tareas."""
        # Crear varias tareas
        task1 = TaskCreate(title="Tarea 1", status=TaskStatus.PENDING, priority=TaskPriority.HIGH)
        task2 = TaskCreate(title="Tarea 2", status=TaskStatus.COMPLETED, priority=TaskPriority.LOW)

        task_service.create_task(task1)
        task_service.create_task(task2)

        stats = task_service.get_statistics()
        assert stats["total"] == 2
        assert "by_status" in stats
        assert "by_priority" in stats

    def test_get_all_tasks_sorted(self, task_service):
        """Prueba que las tareas se devuelven ordenadas por fecha."""
        task1 = TaskCreate(title="Tarea 1")
        task2 = TaskCreate(title="Tarea 2")
        task3 = TaskCreate(title="Tarea 3")

        task_service.create_task(task1)
        task_service.create_task(task2)
        task_service.create_task(task3)

        tasks = task_service.get_all_tasks()
        assert len(tasks) == 3
        # Verificar que están ordenadas por fecha de creación (más reciente primero)
        assert tasks[0].created_at >= tasks[1].created_at
        assert tasks[1].created_at >= tasks[2].created_at
