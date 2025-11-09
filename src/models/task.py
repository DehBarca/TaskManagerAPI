"""
Modelo de datos para Tareas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from .enums import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """Modelo base de tarea con campos comunes."""

    title: str = Field(
        ..., min_length=1, max_length=200, description="Título de la tarea"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Descripción detallada"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM, description="Prioridad de la tarea"
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING, description="Estado de la tarea"
    )
    due_date: Optional[datetime] = Field(None, description="Fecha de vencimiento")

    @validator("title")
    def title_must_not_be_empty(cls, v):
        """Valida que el título no esté vacío."""
        if not v or not v.strip():
            raise ValueError("El título no puede estar vacío")
        return v.strip()

    @validator("due_date")
    def due_date_must_be_future(cls, v):
        """Valida que la fecha de vencimiento sea futura."""
        if v and v < datetime.now():
            raise ValueError("La fecha de vencimiento debe ser en el futuro")
        return v


class TaskCreate(TaskBase):
    """Modelo para crear una nueva tarea."""

    pass


class TaskUpdate(BaseModel):
    """Modelo para actualizar una tarea existente."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None

    @validator("title")
    def title_must_not_be_empty(cls, v):
        """Valida que el título no esté vacío si se proporciona."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("El título no puede estar vacío")
        return v.strip() if v else v


class Task(TaskBase):
    """Modelo completo de tarea incluyendo campos generados."""

    id: str = Field(..., description="Identificador único de la tarea")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Fecha de creación"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Fecha de última actualización"
    )

    class Config:
        """Configuración de Pydantic."""

        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Implementar API REST",
                "description": "Crear endpoints para CRUD de tareas",
                "priority": "high",
                "status": "in_progress",
                "due_date": "2025-12-31T23:59:59",
                "created_at": "2025-11-08T10:00:00",
                "updated_at": "2025-11-08T15:30:00",
            }
        }
