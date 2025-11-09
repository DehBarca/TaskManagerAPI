"""
Pruebas unitarias para los repositorios.
"""

import pytest
from datetime import datetime, timedelta
from src.models import Task, TaskStatus, TaskPriority


class TestTaskRepository:
    """Pruebas para TaskRepository."""

    def test_find_all_empty(self, task_repository):
        """Prueba obtener todas las tareas cuando no hay ninguna."""
        tasks = task_repository.find_all()
        assert len(tasks) == 0

    def test_save_and_find_by_id(self, task_repository):
        """Prueba guardar y buscar una tarea por ID."""
        task = Task(
            id="test-id-1",
            title="Tarea de Prueba",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        saved_task = task_repository.save(task)
        assert saved_task.id == "test-id-1"

        found_task = task_repository.find_by_id("test-id-1")
        assert found_task is not None
        assert found_task.title == "Tarea de Prueba"

    def test_find_by_id_not_found(self, task_repository):
        """Prueba buscar una tarea que no existe."""
        task = task_repository.find_by_id("non-existent-id")
        assert task is None

    def test_find_all_returns_all_tasks(self, task_repository):
        """Prueba que find_all retorna todas las tareas."""
        # Crear varias tareas
        for i in range(5):
            task = Task(
                id=f"task-{i}",
                title=f"Tarea {i}",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            task_repository.save(task)

        tasks = task_repository.find_all()
        assert len(tasks) == 5

    def test_find_by_status(self, task_repository):
        """Prueba buscar tareas por estado."""
        # Crear tareas con diferentes estados
        task1 = Task(
            id="task-1",
            title="Tarea Pendiente",
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        task2 = Task(
            id="task-2",
            title="Tarea Completada",
            status=TaskStatus.COMPLETED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        task_repository.save(task1)
        task_repository.save(task2)

        pending_tasks = task_repository.find_by_status(TaskStatus.PENDING)
        assert len(pending_tasks) == 1
        assert pending_tasks[0].title == "Tarea Pendiente"

    def test_find_by_title(self, task_repository):
        """Prueba buscar una tarea por título."""
        task = Task(
            id="task-1",
            title="Título Único",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        task_repository.save(task)

        found_task = task_repository.find_by_title("Título Único")
        assert found_task is not None
        assert found_task.id == "task-1"

    def test_find_by_title_case_insensitive(self, task_repository):
        """Prueba que la búsqueda por título sea insensible a mayúsculas."""
        task = Task(
            id="task-1",
            title="Título de Prueba",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        task_repository.save(task)

        found_task = task_repository.find_by_title("título de prueba")
        assert found_task is not None

    def test_update_task(self, task_repository):
        """Prueba actualizar una tarea."""
        task = Task(
            id="task-1",
            title="Título Original",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        task_repository.save(task)

        task.title = "Título Actualizado"
        task.status = TaskStatus.COMPLETED
        updated_task = task_repository.update(task)

        assert updated_task.title == "Título Actualizado"
        assert updated_task.status == TaskStatus.COMPLETED

    def test_delete_task(self, task_repository):
        """Prueba eliminar una tarea."""
        task = Task(
            id="task-1",
            title="Tarea a Eliminar",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        task_repository.save(task)

        result = task_repository.delete("task-1")
        assert result is True

        found_task = task_repository.find_by_id("task-1")
        assert found_task is None

    def test_delete_non_existent_task(self, task_repository):
        """Prueba eliminar una tarea que no existe."""
        result = task_repository.delete("non-existent-id")
        assert result is False

    def test_exists(self, task_repository):
        """Prueba verificar si existe una tarea."""
        task = Task(
            id="task-1",
            title="Tarea",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        task_repository.save(task)

        assert task_repository.exists("task-1") is True
        assert task_repository.exists("non-existent") is False

    def test_count(self, task_repository):
        """Prueba contar el número de tareas."""
        assert task_repository.count() == 0

        for i in range(3):
            task = Task(
                id=f"task-{i}",
                title=f"Tarea {i}",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            task_repository.save(task)

        assert task_repository.count() == 3
