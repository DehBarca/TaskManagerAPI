"""
Pruebas de integración para la API REST.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from src.main import app
from src.database import get_database
from src.models import TaskStatus, TaskPriority


@pytest.fixture
def client():
    """Fixture que proporciona un cliente de prueba para la API."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    """Fixture que limpia la base de datos antes de cada prueba."""
    db = get_database()
    db.clear_collection("tasks")
    yield
    db.clear_collection("tasks")


class TestHealthEndpoints:
    """Pruebas para los endpoints de salud."""

    def test_root_endpoint(self, client):
        """Prueba el endpoint raíz."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check(self, client):
        """Prueba el endpoint de health check."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestTaskEndpoints:
    """Pruebas para los endpoints de tareas."""

    def test_get_all_tasks_empty(self, client):
        """Prueba obtener todas las tareas cuando no hay ninguna."""
        response = client.get("/api/v1/tasks/")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_task(self, client):
        """Prueba crear una nueva tarea."""
        task_data = {
            "title": "Nueva Tarea",
            "description": "Descripción de la tarea",
            "priority": "high",
            "status": "pending",
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
        }
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == "Nueva Tarea"
        assert "id" in data
        assert "created_at" in data

    def test_create_task_minimal_data(self, client):
        """Prueba crear una tarea con datos mínimos."""
        task_data = {"title": "Tarea Mínima"}
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == "Tarea Mínima"
        assert data["priority"] == "medium"
        assert data["status"] == "pending"

    def test_create_task_with_empty_title_fails(self, client):
        """Prueba que falla al crear con título vacío."""
        task_data = {"title": "   "}
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 422

    def test_create_duplicate_task_fails(self, client):
        """Prueba que falla al crear una tarea duplicada."""
        task_data = {"title": "Tarea Única"}

        # Primera creación exitosa
        response1 = client.post("/api/v1/tasks/", json=task_data)
        assert response1.status_code == 201

        # Segunda creación falla
        response2 = client.post("/api/v1/tasks/", json=task_data)
        assert response2.status_code == 400

    def test_get_task_by_id(self, client):
        """Prueba obtener una tarea por ID."""
        # Crear tarea
        task_data = {"title": "Tarea de Prueba"}
        create_response = client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Obtener tarea
        response = client.get(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Tarea de Prueba"

    def test_get_task_not_found(self, client):
        """Prueba obtener una tarea que no existe."""
        response = client.get("/api/v1/tasks/non-existent-id")
        assert response.status_code == 404

    def test_update_task(self, client):
        """Prueba actualizar una tarea."""
        # Crear tarea
        task_data = {"title": "Tarea Original"}
        create_response = client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Actualizar tarea
        update_data = {"title": "Tarea Actualizada", "status": "in_progress"}
        response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "Tarea Actualizada"
        assert data["status"] == "in_progress"

    def test_update_task_not_found(self, client):
        """Prueba actualizar una tarea que no existe."""
        update_data = {"title": "Nuevo Título"}
        response = client.put("/api/v1/tasks/non-existent-id", json=update_data)
        assert response.status_code == 404

    def test_delete_task(self, client):
        """Prueba eliminar una tarea."""
        # Crear tarea
        task_data = {"title": "Tarea a Eliminar"}
        create_response = client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Eliminar tarea
        response = client.delete(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 204

        # Verificar que ya no existe
        get_response = client.get(f"/api/v1/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client):
        """Prueba eliminar una tarea que no existe."""
        response = client.delete("/api/v1/tasks/non-existent-id")
        assert response.status_code == 404

    def test_get_tasks_by_status(self, client):
        """Prueba filtrar tareas por estado."""
        # Crear varias tareas con diferentes estados
        client.post("/api/v1/tasks/", json={"title": "Tarea 1", "status": "pending"})
        client.post("/api/v1/tasks/", json={"title": "Tarea 2", "status": "completed"})
        client.post("/api/v1/tasks/", json={"title": "Tarea 3", "status": "pending"})

        # Obtener tareas pendientes
        response = client.get("/api/v1/tasks/status/pending")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 2
        assert all(task["status"] == "pending" for task in data)

    def test_complete_task(self, client):
        """Prueba marcar una tarea como completada."""
        # Crear tarea
        task_data = {"title": "Tarea a Completar"}
        create_response = client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Completar tarea
        response = client.patch(f"/api/v1/tasks/{task_id}/complete")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "completed"

    def test_get_statistics(self, client):
        """Prueba obtener estadísticas."""
        # Crear varias tareas
        client.post(
            "/api/v1/tasks/",
            json={"title": "Tarea 1", "status": "pending", "priority": "high"},
        )
        client.post(
            "/api/v1/tasks/",
            json={"title": "Tarea 2", "status": "completed", "priority": "low"},
        )

        # Obtener estadísticas
        response = client.get("/api/v1/tasks/analytics/statistics")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 2
        assert "by_status" in data
        assert "by_priority" in data
        assert "overdue" in data
