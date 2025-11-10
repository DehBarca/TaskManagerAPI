"""
Excepciones personalizadas de la aplicación.
"""


class TaskManagerError(Exception):
    """Excepción base para todas las excepciones de la aplicación."""

    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class TaskNotFoundException(TaskManagerError):
    """Excepción lanzada cuando no se encuentra una tarea."""

    def __init__(self, task_id: str):
        message = f"Tarea con ID '{task_id}' no encontrada"
        super().__init__(message, {"task_id": task_id})


class TaskValidationException(TaskManagerError):
    """Excepción lanzada cuando falla la validación de una tarea."""

    def __init__(self, message: str, field: str = None):
        details = {"field": field} if field else {}
        super().__init__(message, details)


class DuplicateTaskException(TaskManagerError):
    """Excepción lanzada cuando se intenta crear una tarea duplicada."""

    def __init__(self, title: str):
        message = f"Ya existe una tarea con el título '{title}'"
        super().__init__(message, {"title": title})
