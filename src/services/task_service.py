"""
Servicio de lógica de negocio para tareas.
Contiene toda la lógica de negocio relacionada con tareas.
"""

from typing import List, Optional
from datetime import datetime
import uuid
from ..models import Task, TaskCreate, TaskUpdate, TaskStatus
from ..repositories import TaskRepository
from ..utils.exceptions import (
    TaskNotFoundException,
    TaskValidationException,
    DuplicateTaskException,
)
from ..utils.logger import get_logger

logger = get_logger(__name__)


class TaskService:
    """Servicio para la lógica de negocio de tareas."""

    def __init__(self, repository: TaskRepository):
        """
        Inicializa el servicio.

        Args:
            repository: Repositorio de tareas.
        """
        self.repository = repository

    def get_all_tasks(self) -> List[Task]:
        """
        Obtiene todas las tareas ordenadas por fecha de creación.

        Returns:
            Lista de todas las tareas.
        """
        logger.info("Obteniendo todas las tareas")
        tasks = self.repository.find_all()
        # Ordenar por fecha de creación descendente
        tasks.sort(key=lambda x: x.created_at, reverse=True)
        return tasks

    def get_task_by_id(self, task_id: str) -> Task:
        """
        Obtiene una tarea por su ID.

        Args:
            task_id: ID de la tarea.

        Returns:
            Tarea encontrada.

        Raises:
            TaskNotFoundException: Si la tarea no existe.
        """
        logger.info(f"Buscando tarea: {task_id}")
        task = self.repository.find_by_id(task_id)
        if not task:
            logger.warning(f"Tarea no encontrada: {task_id}")
            raise TaskNotFoundException(task_id)
        return task

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """
        Obtiene tareas filtradas por estado.

        Args:
            status: Estado de las tareas a buscar.

        Returns:
            Lista de tareas con el estado especificado.
        """
        logger.info(f"Buscando tareas con estado: {status}")
        tasks = self.repository.find_by_status(status)
        tasks.sort(key=lambda x: x.created_at, reverse=True)
        return tasks

    def create_task(self, task_data: TaskCreate) -> Task:
        """
        Crea una nueva tarea.

        Args:
            task_data: Datos de la nueva tarea.

        Returns:
            Tarea creada.

        Raises:
            DuplicateTaskException: Si ya existe una tarea con el mismo título.
            TaskValidationException: Si los datos son inválidos.
        """
        logger.info(f"Creando nueva tarea: {task_data.title}")

        # Verificar si ya existe una tarea con el mismo título
        existing_task = self.repository.find_by_title(task_data.title)
        if existing_task:
            logger.warning(f"Intento de crear tarea duplicada: {task_data.title}")
            raise DuplicateTaskException(task_data.title)

        # Validación adicional de negocio
        if task_data.due_date and task_data.due_date < datetime.now():
            raise TaskValidationException(
                "La fecha de vencimiento no puede ser en el pasado", field="due_date"
            )

        # Crear la tarea
        task = Task(
            id=str(uuid.uuid4()),
            **task_data.model_dump(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        saved_task = self.repository.save(task)
        logger.info(f"Tarea creada exitosamente: {saved_task.id}")
        return saved_task

    def update_task(self, task_id: str, task_data: TaskUpdate) -> Task:
        """
        Actualiza una tarea existente.

        Args:
            task_id: ID de la tarea a actualizar.
            task_data: Datos actualizados.

        Returns:
            Tarea actualizada.

        Raises:
            TaskNotFoundException: Si la tarea no existe.
            TaskValidationException: Si los datos son inválidos.
        """
        logger.info(f"Actualizando tarea: {task_id}")

        # Obtener la tarea existente
        existing_task = self.get_task_by_id(task_id)

        # Preparar datos actualizados
        update_data = task_data.model_dump(exclude_unset=True)

        # Validaciones de negocio
        if "title" in update_data:
            other_task = self.repository.find_by_title(update_data["title"])
            if other_task and other_task.id != task_id:
                raise DuplicateTaskException(update_data["title"])

        if "due_date" in update_data and update_data["due_date"]:
            if update_data["due_date"] < datetime.now():
                raise TaskValidationException(
                    "La fecha de vencimiento no puede ser en el pasado",
                    field="due_date",
                )

        # Aplicar actualizaciones
        for key, value in update_data.items():
            setattr(existing_task, key, value)

        updated_task = self.repository.update(existing_task)
        logger.info(f"Tarea actualizada exitosamente: {task_id}")
        return updated_task

    def delete_task(self, task_id: str) -> bool:
        """
        Elimina una tarea.

        Args:
            task_id: ID de la tarea a eliminar.

        Returns:
            True si se eliminó correctamente.

        Raises:
            TaskNotFoundException: Si la tarea no existe.
        """
        logger.info(f"Eliminando tarea: {task_id}")

        # Verificar que existe
        self.get_task_by_id(task_id)

        # Eliminar
        result = self.repository.delete(task_id)
        if result:
            logger.info(f"Tarea eliminada exitosamente: {task_id}")
        return result

    def complete_task(self, task_id: str) -> Task:
        """
        Marca una tarea como completada.

        Args:
            task_id: ID de la tarea.

        Returns:
            Tarea actualizada.

        Raises:
            TaskNotFoundException: Si la tarea no existe.
        """
        logger.info(f"Marcando tarea como completada: {task_id}")
        task_update = TaskUpdate(status=TaskStatus.COMPLETED)
        return self.update_task(task_id, task_update)

    def get_statistics(self) -> dict:
        """
        Obtiene estadísticas sobre las tareas.

        Returns:
            Diccionario con estadísticas.
        """
        logger.info("Obteniendo estadísticas de tareas")
        all_tasks = self.repository.find_all()

        stats = {
            "total": len(all_tasks),
            "by_status": {},
            "by_priority": {},
            "overdue": 0,
        }

        now = datetime.now()
        for task in all_tasks:
            # Contar por estado
            status_key = task.status.value
            stats["by_status"][status_key] = stats["by_status"].get(status_key, 0) + 1

            # Contar por prioridad
            priority_key = task.priority.value
            stats["by_priority"][priority_key] = (
                stats["by_priority"].get(priority_key, 0) + 1
            )

            # Contar vencidas
            if (
                task.due_date
                and task.due_date < now
                and task.status != TaskStatus.COMPLETED
            ):
                stats["overdue"] += 1

        return stats
