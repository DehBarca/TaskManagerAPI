"""
Repositorio para el acceso a datos de tareas.
Implementa el patrón Repository para abstraer la capa de persistencia.
"""

from datetime import datetime

from ..database import Database
from ..models import Task, TaskStatus
from ..utils.logger import get_logger

logger = get_logger(__name__)


class TaskRepository:
    """Repositorio para operaciones CRUD de tareas."""

    COLLECTION = "tasks"

    def __init__(self, database: Database):
        """
        Inicializa el repositorio.

        Args:
            database: Instancia de la base de datos.
        """
        self.db = database

    def find_all(self) -> list[Task]:
        """
        Obtiene todas las tareas.

        Returns:
            Lista de todas las tareas.
        """
        tasks_data = self.db.get_all(self.COLLECTION)
        tasks = [Task(**data) for data in tasks_data.values()]
        logger.info(f"Se encontraron {len(tasks)} tareas")
        return tasks

    def find_by_id(self, task_id: str) -> Task | None:
        """
        Busca una tarea por su ID.

        Args:
            task_id: ID de la tarea.

        Returns:
            Tarea encontrada o None.
        """
        task_data = self.db.get_by_id(self.COLLECTION, task_id)
        if task_data:
            logger.debug(f"Tarea encontrada: {task_id}")
            return Task(**task_data)
        logger.debug(f"Tarea no encontrada: {task_id}")
        return None

    def find_by_status(self, status: TaskStatus) -> list[Task]:
        """
        Busca tareas por estado.

        Args:
            status: Estado de la tarea.

        Returns:
            Lista de tareas con el estado especificado.
        """
        all_tasks = self.find_all()
        filtered_tasks = [task for task in all_tasks if task.status == status]
        logger.info(f"Se encontraron {len(filtered_tasks)} tareas con estado '{status}'")
        return filtered_tasks

    def find_by_title(self, title: str) -> Task | None:
        """
        Busca una tarea por título exacto.

        Args:
            title: Título de la tarea.

        Returns:
            Tarea encontrada o None.
        """
        all_tasks = self.find_all()
        for task in all_tasks:
            if task.title.lower() == title.lower():
                return task
        return None

    def save(self, task: Task) -> Task:
        """
        Guarda una nueva tarea.

        Args:
            task: Tarea a guardar.

        Returns:
            Tarea guardada.
        """
        task_dict = task.model_dump()
        # Convertir datetime a string para serialización JSON
        task_dict["created_at"] = task.created_at.isoformat()
        task_dict["updated_at"] = task.updated_at.isoformat()
        if task.due_date:
            task_dict["due_date"] = task.due_date.isoformat()

        self.db.insert(self.COLLECTION, task.id, task_dict)
        logger.info(f"Tarea guardada: {task.id}")
        return task

    def update(self, task: Task) -> Task:
        """
        Actualiza una tarea existente.

        Args:
            task: Tarea con los datos actualizados.

        Returns:
            Tarea actualizada.
        """
        task.updated_at = datetime.now()
        task_dict = task.model_dump()
        # Convertir datetime a string para serialización JSON
        task_dict["created_at"] = task.created_at.isoformat()
        task_dict["updated_at"] = task.updated_at.isoformat()
        if task.due_date:
            task_dict["due_date"] = task.due_date.isoformat()

        self.db.update(self.COLLECTION, task.id, task_dict)
        logger.info(f"Tarea actualizada: {task.id}")
        return task

    def delete(self, task_id: str) -> bool:
        """
        Elimina una tarea.

        Args:
            task_id: ID de la tarea a eliminar.

        Returns:
            True si se eliminó, False si no existía.
        """
        result = self.db.delete(self.COLLECTION, task_id)
        if result:
            logger.info(f"Tarea eliminada: {task_id}")
        else:
            logger.warning(f"Intento de eliminar tarea inexistente: {task_id}")
        return result

    def exists(self, task_id: str) -> bool:
        """
        Verifica si existe una tarea con el ID dado.

        Args:
            task_id: ID de la tarea.

        Returns:
            True si existe, False en caso contrario.
        """
        return self.find_by_id(task_id) is not None

    def count(self) -> int:
        """
        Cuenta el número total de tareas.

        Returns:
            Número de tareas.
        """
        return len(self.db.get_all(self.COLLECTION))
