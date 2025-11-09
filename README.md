# Task Manager API

Una aplicación robusta de gestión de tareas construida con FastAPI.

## 🏗️ Arquitectura

El proyecto sigue una arquitectura en capas:

- **Models**: Modelos de datos con validación usando Pydantic
- **Repositories**: Capa de acceso a datos con patrón Repository
- **Services**: Lógica de negocio
- **API**: Endpoints REST con FastAPI
- **Utils**: Utilidades y helpers

## 📋 Características

- ✅ CRUD completo de tareas
- ✅ Validación de datos con Pydantic
- ✅ Manejo de errores personalizado
- ✅ Logging estructurado
- ✅ Pruebas unitarias con alta cobertura
- ✅ Documentación automática con Swagger
- ✅ Configuración mediante variables de entorno

## 🚀 Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
```bash
python -m venv venv
```

3. Activar el entorno virtual:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Configurar variables de entorno:
```bash
cp .env.example .env
```

## 🏃 Ejecución

```bash
python src/main.py
```

La API estará disponible en: http://localhost:8000

Documentación interactiva: http://localhost:8000/docs

## 🧪 Pruebas

Ejecutar todas las pruebas:
```bash
pytest
```

Con cobertura:
```bash
pytest --cov=src --cov-report=html
```

## 📚 API Endpoints

### Tareas

- `GET /api/v1/tasks` - Listar todas las tareas
- `GET /api/v1/tasks/{task_id}` - Obtener una tarea específica
- `POST /api/v1/tasks` - Crear una nueva tarea
- `PUT /api/v1/tasks/{task_id}` - Actualizar una tarea
- `DELETE /api/v1/tasks/{task_id}` - Eliminar una tarea
- `GET /api/v1/tasks/status/{status}` - Filtrar tareas por estado

### Health Check

- `GET /health` - Verificar estado de la aplicación

## 🗂️ Estructura del Proyecto

```
ProjectoSoftware/
├── src/
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── config.py               # Configuración de la aplicación
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py             # Modelo de Tarea
│   │   └── enums.py            # Enumeraciones
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py     # Lógica de negocio de tareas
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── task_repository.py  # Acceso a datos
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py           # Definición de rutas
│   │   └── dependencies.py     # Dependencias de FastAPI
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── exceptions.py       # Excepciones personalizadas
│   │   └── logger.py           # Configuración de logging
│   └── database/
│       ├── __init__.py
│       └── connection.py       # Configuración de base de datos
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Configuración de pytest
│   ├── test_models.py          # Pruebas de modelos
│   ├── test_services.py        # Pruebas de servicios
│   ├── test_repositories.py    # Pruebas de repositorios
│   └── test_api.py             # Pruebas de API
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Pydantic**: Validación de datos
- **SQLAlchemy**: ORM para base de datos
- **Pytest**: Framework de pruebas
- **Uvicorn**: Servidor ASGI
