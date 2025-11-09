"""
Definición de rutas de la API REST.
"""

from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from ..models import Task, TaskCreate, TaskUpdate, TaskStatus
from ..services import TaskService
from ..utils.exceptions import (
    TaskNotFoundException,
    TaskValidationException,
    DuplicateTaskException,
)
from .dependencies import get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[Task], summary="Listar todas las tareas")
async def get_all_tasks(
    service: Annotated[TaskService, Depends(get_task_service)],
) -> List[Task]:
    """
    Obtiene todas las tareas del sistema.

    Returns:
        Lista de todas las tareas ordenadas por fecha de creación.
    """
    return service.get_all_tasks()


@router.get("/{task_id}", response_model=Task, summary="Obtener una tarea")
async def get_task(
    task_id: str, service: Annotated[TaskService, Depends(get_task_service)]
) -> Task:
    """
    Obtiene una tarea específica por su ID.

    Args:
        task_id: ID de la tarea.

    Returns:
        Tarea encontrada.

    Raises:
        HTTPException: 404 si la tarea no existe.
    """
    try:
        return service.get_task_by_id(task_id)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.get(
    "/status/{task_status}",
    response_model=List[Task],
    summary="Filtrar tareas por estado",
)
async def get_tasks_by_status(
    task_status: TaskStatus, service: Annotated[TaskService, Depends(get_task_service)]
) -> List[Task]:
    """
    Obtiene tareas filtradas por estado.

    Args:
        task_status: Estado de las tareas (pending, in_progress, completed, cancelled).

    Returns:
        Lista de tareas con el estado especificado.
    """
    return service.get_tasks_by_status(task_status)


@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva tarea",
)
async def create_task(
    task_data: TaskCreate, service: Annotated[TaskService, Depends(get_task_service)]
) -> Task:
    """
    Crea una nueva tarea.

    Args:
        task_data: Datos de la nueva tarea.

    Returns:
        Tarea creada.

    Raises:
        HTTPException: 400 si los datos son inválidos o la tarea ya existe.
    """
    try:
        return service.create_task(task_data)
    except (DuplicateTaskException, TaskValidationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.put("/{task_id}", response_model=Task, summary="Actualizar una tarea")
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    service: Annotated[TaskService, Depends(get_task_service)],
) -> Task:
    """
    Actualiza una tarea existente.

    Args:
        task_id: ID de la tarea a actualizar.
        task_data: Datos actualizados de la tarea.

    Returns:
        Tarea actualizada.

    Raises:
        HTTPException: 404 si la tarea no existe, 400 si los datos son inválidos.
    """
    try:
        return service.update_task(task_id, task_data)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except (DuplicateTaskException, TaskValidationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.delete(
    "/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una tarea"
)
async def delete_task(
    task_id: str, service: Annotated[TaskService, Depends(get_task_service)]
):
    """
    Elimina una tarea.

    Args:
        task_id: ID de la tarea a eliminar.

    Raises:
        HTTPException: 404 si la tarea no existe.
    """
    try:
        service.delete_task(task_id)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.patch(
    "/{task_id}/complete", response_model=Task, summary="Marcar tarea como completada"
)
async def complete_task(
    task_id: str, service: Annotated[TaskService, Depends(get_task_service)]
) -> Task:
    """
    Marca una tarea como completada.

    Args:
        task_id: ID de la tarea.

    Returns:
        Tarea actualizada.

    Raises:
        HTTPException: 404 si la tarea no existe.
    """
    try:
        return service.complete_task(task_id)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.get("/analytics/statistics", summary="Obtener estadísticas")
async def get_statistics(
    service: Annotated[TaskService, Depends(get_task_service)],
) -> dict:
    """
    Obtiene estadísticas sobre las tareas.

    Returns:
        Diccionario con estadísticas de tareas.
    """
    return service.get_statistics()
