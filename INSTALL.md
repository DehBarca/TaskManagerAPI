# Instalación y ejecución del proyecto

## Instalación rápida

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python src/main.py
```

## Ejecutar pruebas

```powershell
# Todas las pruebas
pytest

# Con cobertura
pytest --cov=src --cov-report=html

# Ver reporte de cobertura
start htmlcov/index.html
```

## Ejemplos de uso de la API

### Crear una tarea
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar login",
    "description": "Crear sistema de autenticación",
    "priority": "high",
    "due_date": "2025-12-31T23:59:59"
  }'
```

### Listar todas las tareas
```bash
curl "http://localhost:8000/api/v1/tasks/"
```

### Obtener una tarea
```bash
curl "http://localhost:8000/api/v1/tasks/{task_id}"
```

### Actualizar una tarea
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/{task_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

### Completar una tarea
```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/{task_id}/complete"
```

### Eliminar una tarea
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/{task_id}"
```

### Obtener estadísticas
```bash
curl "http://localhost:8000/api/v1/tasks/analytics/statistics"
```
