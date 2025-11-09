"""
Enumeraciones utilizadas en los modelos.
"""

from enum import Enum


class TaskStatus(str, Enum):
    """Estados posibles de una tarea."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Niveles de prioridad de una tarea."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
