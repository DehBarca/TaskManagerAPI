# 📘 Guía de Estilo de Código - TaskManagerAPI

## 🎯 Objetivo

Esta guía establece las convenciones y mejores prácticas que todo el equipo debe seguir al contribuir al proyecto TaskManagerAPI. El cumplimiento de estas reglas es validado automáticamente por **Ruff** (linter) y **SonarQube** (análisis de calidad).

---

## 📋 Tabla de Contenido

1. [Convenciones de Nombres](#1-convenciones-de-nombres)
2. [Formato y Estructura](#2-formato-y-estructura)
3. [Funciones y Métodos](#3-funciones-y-métodos)
4. [Documentación](#4-documentación)
5. [Imports](#5-imports)
6. [Manejo de Errores](#6-manejo-de-errores)
7. [Complejidad del Código](#7-complejidad-del-código)
8. [Tests](#8-tests)
9. [Seguridad](#9-seguridad)
10. [Quality Gates](#10-quality-gates)

---

## 1. Convenciones de Nombres

### 1.1 Variables y Funciones
- **snake_case** para variables y funciones
- Nombres descriptivos y significativos
- Evitar abreviaturas no estándar

```python
# ✅ CORRECTO
def get_all_tasks() -> list[Task]:
    task_list = []
    max_retries = 3
    is_active = True

# ❌ INCORRECTO
def GetAllTasks():  # No usar PascalCase
    taskList = []   # No usar camelCase
    mr = 3          # Abreviatura no clara
    a = True        # Nombre no descriptivo
```

**Regla Ruff:** `N802`, `N803`, `N806`  
**Regla SonarQube:** `python:S117` (Nombres de variables)

### 1.2 Clases
- **PascalCase** para nombres de clases
- Sustantivos descriptivos

```python
# ✅ CORRECTO
class TaskService:
    pass

class TaskRepository:
    pass

# ❌ INCORRECTO
class task_service:  # No usar snake_case
    pass

class Svc:  # Nombre no descriptivo
    pass
```

**Regla Ruff:** `N801`  
**Regla SonarQube:** `python:S101` (Nombres de clases)

### 1.3 Constantes
- **UPPER_CASE** con guiones bajos
- Definir al inicio del módulo

```python
# ✅ CORRECTO
MAX_TASKS_PER_USER = 100
DEFAULT_TIMEOUT = 30
API_VERSION = "1.0.0"

# ❌ INCORRECTO
maxTasksPerUser = 100  # No usar camelCase
max_tasks = 100        # No usar snake_case para constantes
```

**Regla Ruff:** `N806`  
**Regla SonarQube:** `python:S1192` (Constantes mágicas)

### 1.4 Métodos Privados
- Prefijo con un guion bajo `_`
- Solo para uso interno de la clase

```python
# ✅ CORRECTO
class TaskService:
    def _validate_task_data(self, data: dict) -> bool:
        """Método privado de validación."""
        return True
    
    def create_task(self, data: dict) -> Task:
        """Método público."""
        if self._validate_task_data(data):
            return Task(**data)

# ❌ INCORRECTO
class TaskService:
    def validateTaskData(self, data: dict) -> bool:  # Debería ser privado
        return True
```

**Regla Ruff:** `N807`

### 1.5 Excepciones
- Sufijo `Error` o `Exception`
- Heredar de `Exception` o sus subclases

```python
# ✅ CORRECTO
class TaskNotFoundError(Exception):
    pass

class TaskValidationException(Exception):
    pass

# ❌ INCORRECTO
class TaskNotFound:  # Falta sufijo
    pass

class task_error(Exception):  # No usar snake_case
    pass
```

**Regla Ruff:** `N818`  
**Regla SonarQube:** `python:S3776` (Excepciones personalizadas)

---

## 2. Formato y Estructura

### 2.1 Longitud de Líneas
- **Máximo 100 caracteres** por línea
- Dividir líneas largas de forma legible

```python
# ✅ CORRECTO
def create_task(
    title: str,
    description: str | None = None,
    priority: TaskPriority = TaskPriority.MEDIUM,
) -> Task:
    return Task(title=title, description=description, priority=priority)

# ❌ INCORRECTO
def create_task(title: str, description: str | None = None, priority: TaskPriority = TaskPriority.MEDIUM) -> Task:  # > 100 caracteres
    return Task(title=title, description=description, priority=priority)
```

**Regla Ruff:** `E501`  
**Regla SonarQube:** `python:S103` (Longitud de línea)

### 2.2 Indentación
- **4 espacios** (NO tabs)
- Consistente en todo el proyecto

```python
# ✅ CORRECTO
def process_task(task: Task) -> None:
    if task.status == TaskStatus.PENDING:
        task.status = TaskStatus.IN_PROGRESS
        task.save()

# ❌ INCORRECTO
def process_task(task: Task) -> None:
  if task.status == TaskStatus.PENDING:  # 2 espacios
      task.status = TaskStatus.IN_PROGRESS  # Mezclando 2 y 4 espacios
	task.save()  # Tab
```

**Regla Ruff:** `E111`, `E112`, `E113`  
**Regla SonarQube:** `python:S1656` (Indentación)

### 2.3 Espacios en Blanco
- 2 líneas en blanco entre funciones de nivel superior
- 1 línea en blanco entre métodos de clase
- No espacios en blanco al final de líneas

```python
# ✅ CORRECTO
def function_one():
    pass


def function_two():
    pass


class MyClass:
    def method_one(self):
        pass
    
    def method_two(self):
        pass

# ❌ INCORRECTO
def function_one():
    pass
def function_two():  # Falta línea en blanco
    pass
```

**Regla Ruff:** `E301`, `E302`, `E303`, `W291`

### 2.4 Comillas
- **Comillas dobles `"`** para strings
- Comillas simples `'` solo para casos especiales

```python
# ✅ CORRECTO
message = "Tarea creada exitosamente"
query = 'SELECT * FROM tasks WHERE title = "Important"'  # Caso especial

# ❌ INCORRECTO
message = 'Tarea creada exitosamente'  # Usar comillas dobles
```

**Regla Ruff:** Configurado en `quote-style = "double"`

---

## 3. Funciones y Métodos

### 3.1 Tamaño de Funciones
- **Máximo 50 líneas** por función
- Si es más larga, refactorizar en funciones más pequeñas

```python
# ✅ CORRECTO
def create_task(self, task_data: TaskCreate) -> Task:
    """Crea una nueva tarea (< 50 líneas)."""
    self._validate_task(task_data)
    task = self._build_task(task_data)
    return self._save_task(task)

def _validate_task(self, task_data: TaskCreate) -> None:
    """Validación separada."""
    if not task_data.title:
        raise ValueError("Title required")

# ❌ INCORRECTO
def create_task(self, task_data: TaskCreate) -> Task:
    # 80 líneas de código mezclando validación, construcción,
    # guardado, notificaciones, logs, etc.
    ...  # Demasiado larga, difícil de mantener
```

**Regla SonarQube:** `python:S138` (Funciones demasiado largas)

### 3.2 Parámetros de Funciones
- **Máximo 5 parámetros** por función
- Usar dataclasses o Pydantic models para más parámetros

```python
# ✅ CORRECTO
def create_task(self, task_data: TaskCreate) -> Task:
    pass

# Aceptable (≤ 5 parámetros)
def filter_tasks(
    status: TaskStatus,
    priority: TaskPriority,
    start_date: datetime,
    end_date: datetime,
    user_id: str,
) -> list[Task]:
    pass

# ❌ INCORRECTO
def create_task(
    title: str,
    description: str,
    priority: TaskPriority,
    status: TaskStatus,
    due_date: datetime,
    created_by: str,
    tags: list[str],
) -> Task:  # Demasiados parámetros, usar modelo
    pass
```

**Regla SonarQube:** `python:S107` (Demasiados parámetros)

### 3.3 Valores de Retorno
- **Un solo tipo** de retorno por función
- Evitar retornar `None` y otro tipo mezclados cuando sea posible

```python
# ✅ CORRECTO
def find_task(self, task_id: str) -> Task:
    """Retorna Task o lanza excepción."""
    task = self.repository.find_by_id(task_id)
    if not task:
        raise TaskNotFoundException(task_id)
    return task

# ⚠️ Aceptable pero menos preferible
def find_task(self, task_id: str) -> Task | None:
    """Retorna Task o None."""
    return self.repository.find_by_id(task_id)

# ❌ INCORRECTO
def process_task(self, task_id: str) -> Task | bool | None:
    """Múltiples tipos no relacionados."""
    ...
```

**Regla Ruff:** Type hints requeridos  
**Regla SonarQube:** `python:S1763` (Inconsistencia en retornos)

---

## 4. Documentación

### 4.1 Docstrings
- **Obligatorio** para todas las funciones públicas
- Formato: descripción + Args + Returns + Raises

```python
# ✅ CORRECTO
def create_task(self, task_data: TaskCreate) -> Task:
    """
    Crea una nueva tarea en el sistema.
    
    Args:
        task_data: Datos de la tarea a crear.
    
    Returns:
        La tarea creada con ID generado.
    
    Raises:
        DuplicateTaskException: Si ya existe una tarea con el mismo título.
        TaskValidationException: Si los datos son inválidos.
    """
    ...

# ❌ INCORRECTO
def create_task(self, task_data: TaskCreate) -> Task:
    # Sin docstring
    ...

def create_task(self, task_data: TaskCreate) -> Task:
    """Crea tarea"""  # Docstring muy corto, sin Args/Returns
    ...
```

**Regla Ruff:** `D100`, `D101`, `D102`, `D103`  
**Regla SonarQube:** `python:S1542` (Funciones sin documentación)

### 4.2 Comentarios
- Explicar el **"por qué"**, no el **"qué"**
- Comentarios en línea solo cuando sea necesario

```python
# ✅ CORRECTO
# Usar UUID v4 para garantizar unicidad global sin colisiones
task_id = str(uuid.uuid4())

# Validación temprana para evitar costos de DB
if not task_data.title:
    raise ValueError("Title required")

# ❌ INCORRECTO
# Incrementar contador
counter += 1  # Obvio, no necesita comentario

# Llamar a la función save
task.save()  # No aporta valor
```

**Regla SonarQube:** `python:S125` (Código comentado)

### 4.3 TODOs
- Formato: `# TODO: descripción`
- Siempre con descripción clara

```python
# ✅ CORRECTO
# TODO: Implementar paginación cuando haya más de 1000 tareas
def get_all_tasks(self) -> list[Task]:
    return self.repository.find_all()

# TODO: Añadir rate limiting después del MVP
@router.post("/tasks")
def create_task(...):
    pass

# ❌ INCORRECTO
# TODO: Fix
# TODO
```

**Regla Ruff:** `T100`

---

## 5. Imports

### 5.1 Ordenamiento
- Ordenados alfabéticamente
- Agrupados: stdlib → third-party → local

```python
# ✅ CORRECTO
import json
import sys
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.models import Task
from src.services import TaskService

# ❌ INCORRECTO
from src.models import Task
import sys
from fastapi import FastAPI
import json  # Desordenado
```

**Regla Ruff:** `I001` (isort)  
**Regla SonarQube:** `python:S2208` (Imports)

### 5.2 Imports No Usados
- **Prohibido** dejar imports sin usar
- Limpiar automáticamente

```python
# ✅ CORRECTO
from datetime import datetime
from src.models import Task

def process_task(task: Task) -> None:
    task.updated_at = datetime.now()

# ❌ INCORRECTO
from datetime import datetime
from typing import Optional  # No usado
from src.models import Task, Priority  # Priority no usado

def process_task(task: Task) -> None:
    task.updated_at = datetime.now()
```

**Regla Ruff:** `F401`  
**Regla SonarQube:** `python:S1481` (Variables no usadas)

---

## 6. Manejo de Errores

### 6.1 Excepciones Específicas
- Usar excepciones específicas, no genéricas
- Nunca usar `except:` solo

```python
# ✅ CORRECTO
try:
    task = self.repository.find_by_id(task_id)
except TaskNotFoundException as e:
    logger.error(f"Task not found: {task_id}")
    raise HTTPException(status_code=404, detail=str(e)) from e

# ❌ INCORRECTO
try:
    task = self.repository.find_by_id(task_id)
except:  # Demasiado genérico
    pass

try:
    task = self.repository.find_by_id(task_id)
except Exception:  # Muy genérico
    pass
```

**Regla Ruff:** `E722`, `B001`  
**Regla SonarQube:** `python:S1181` (Excepciones genéricas)

### 6.2 Contexto de Excepciones
- Usar `raise ... from e` para preservar contexto

```python
# ✅ CORRECTO
try:
    result = api.call()
except APIError as e:
    raise TaskServiceError("API call failed") from e

# ❌ INCORRECTO
try:
    result = api.call()
except APIError as e:
    raise TaskServiceError("API call failed")  # Pierde contexto
```

**Regla Ruff:** `B904`  
**Regla SonarQube:** `python:S3984` (Cadena de excepciones)

---

## 7. Complejidad del Código

### 7.1 Complejidad Ciclomática
- **Máximo 10** por función
- Refactorizar si supera el límite

```python
# ✅ CORRECTO (Complejidad = 3)
def validate_task(self, task: Task) -> bool:
    if not task.title:
        return False
    if task.due_date and task.due_date < datetime.now():
        return False
    if task.priority not in TaskPriority:
        return False
    return True

# ❌ INCORRECTO (Complejidad > 10)
def complex_validation(self, task: Task) -> bool:
    if condition1:
        if condition2:
            if condition3:
                if condition4:
                    if condition5:
                        if condition6:
                            if condition7:
                                # ... muy complejo
                                pass
```

**Regla Ruff:** `C901` (mccabe)  
**Regla SonarQube:** `python:S3776` (Complejidad cognitiva)

### 7.2 Anidamiento
- **Máximo 4 niveles** de anidamiento
- Usar early returns para reducir anidamiento

```python
# ✅ CORRECTO (Early returns)
def process_task(self, task: Task) -> None:
    if not task:
        return
    
    if not task.is_valid():
        logger.error("Invalid task")
        return
    
    if task.status != TaskStatus.PENDING:
        return
    
    self._execute_task(task)

# ❌ INCORRECTO (Anidamiento profundo)
def process_task(self, task: Task) -> None:
    if task:
        if task.is_valid():
            if task.status == TaskStatus.PENDING:
                if self.can_execute(task):
                    self._execute_task(task)
```

**Regla Ruff:** `SIM102`  
**Regla SonarQube:** `python:S134` (Profundidad de anidamiento)

### 7.3 Duplicación de Código
- **Máximo 3% de código duplicado**
- Extraer a funciones comunes

```python
# ✅ CORRECTO
def _validate_date(self, date: datetime, field_name: str) -> None:
    if date < datetime.now():
        raise ValidationError(f"{field_name} must be in future")

def validate_start_date(self, date: datetime) -> None:
    self._validate_date(date, "start_date")

def validate_end_date(self, date: datetime) -> None:
    self._validate_date(date, "end_date")

# ❌ INCORRECTO (Código duplicado)
def validate_start_date(self, date: datetime) -> None:
    if date < datetime.now():
        raise ValidationError("start_date must be in future")

def validate_end_date(self, date: datetime) -> None:
    if date < datetime.now():
        raise ValidationError("end_date must be in future")
```

**Regla SonarQube:** `python:S1192`, `python:S3776` (Duplicación)

---

## 8. Tests

### 8.1 Cobertura
- **Mínimo 80%** de cobertura de código
- **Objetivo 90%+**

```python
# Todos los casos deben tener tests:
# ✅ Casos exitosos
# ✅ Casos de error
# ✅ Casos edge
# ✅ Validaciones
```

**Regla SonarQube:** Coverage configurado en Quality Gate

### 8.2 Nomenclatura de Tests
- Prefijo `test_`
- Nombre descriptivo del comportamiento

```python
# ✅ CORRECTO
def test_create_task_with_valid_data_succeeds():
    pass

def test_create_task_with_duplicate_title_fails():
    pass

def test_get_task_by_id_not_found_raises_exception():
    pass

# ❌ INCORRECTO
def test1():
    pass

def testTask():
    pass
```

**Regla Ruff:** `PT001` (pytest naming)

### 8.3 Estructura de Tests
- **Arrange-Act-Assert** pattern
- Un concepto por test

```python
# ✅ CORRECTO
def test_create_task_increments_task_count():
    # Arrange
    service = TaskService()
    initial_count = service.count()
    task_data = TaskCreate(title="Test")
    
    # Act
    service.create_task(task_data)
    
    # Assert
    assert service.count() == initial_count + 1

# ❌ INCORRECTO
def test_multiple_things():
    # Testing creation, update, deletion in one test
    task = create_task()
    update_task()
    delete_task()
    # Difícil de debuggear si falla
```

**Regla SonarQube:** `python:S2699` (Tests sin asserts)

---

## 9. Seguridad

### 9.1 Secretos
- **Nunca** hardcodear secretos
- Usar variables de entorno

```python
# ✅ CORRECTO
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# ❌ INCORRECTO
API_KEY = "sk_live_123456789"  # Hardcoded
DATABASE_URL = "postgresql://user:password@localhost/db"
```

**Regla Ruff:** `S105`, `S106`  
**Regla SonarQube:** `python:S2068` (Credenciales hardcoded)

### 9.2 SQL Injection
- Usar ORMs o prepared statements
- Nunca concatenar strings para SQL

```python
# ✅ CORRECTO
def find_by_title(self, title: str) -> Task | None:
    query = "SELECT * FROM tasks WHERE title = ?"
    return db.execute(query, (title,))

# ❌ INCORRECTO
def find_by_title(self, title: str) -> Task | None:
    query = f"SELECT * FROM tasks WHERE title = '{title}'"  # SQL Injection
    return db.execute(query)
```

**Regla SonarQube:** `python:S2077` (SQL Injection)

---

## 10. Quality Gates

### 10.1 Métricas Requeridas

| Métrica | Umbral | Descripción |
|---------|--------|-------------|
| **Cobertura** | ≥ 80% | Porcentaje de código cubierto por tests |
| **Duplicación** | ≤ 3% | Porcentaje de código duplicado |
| **Maintainability** | ≥ A | Rating de mantenibilidad |
| **Reliability** | ≥ A | Rating de confiabilidad (bugs) |
| **Security** | ≥ A | Rating de seguridad (vulnerabilidades) |
| **Complejidad** | ≤ 10 | Complejidad ciclomática por función |
| **Issues Críticos** | 0 | Bloqueantes y críticos deben ser 0 |

### 10.2 Criterios de Aceptación

Para que un PR sea aceptado:

1. ✅ **Todos los tests pasan** (54/54)
2. ✅ **Cobertura ≥ 80%** (actual: 93%)
3. ✅ **0 errores de linting** (Ruff)
4. ✅ **Quality Gate PASSED** (SonarQube)
5. ✅ **0 issues críticos/bloqueantes**
6. ✅ **Code review aprobado** (mínimo 1 aprobación)

---

## 📊 Herramientas de Validación

### Automatización Local

```powershell
# 1. Linting
.\run-linter.ps1

# 2. Tests con cobertura
pytest --cov=src --cov-report=html

# 3. Análisis de SonarQube
.\run-sonar-docker.ps1
```

### Pipeline CI/CD

El pipeline automáticamente verifica:

1. **Instalación de dependencias**
2. **Linting con Ruff** → genera `ruff-report.json`
3. **Tests con cobertura** → genera `coverage.xml`
4. **Análisis SonarQube** → consume reportes
5. **Quality Gate check** → bloquea si falla

---

## 🔄 Proceso de Revisión

### Antes de Commit

```powershell
# 1. Arreglar problemas de estilo
.\run-linter.ps1 -Fix -Format

# 2. Ejecutar tests
pytest

# 3. Verificar cobertura
pytest --cov=src --cov-report=term-missing
```

### Antes de PR

```powershell
# 1. Análisis completo local
.\run-sonar-docker.ps1

# 2. Revisar dashboard
# http://localhost:9000/dashboard?id=TaskManagerAPI
```

### Durante Code Review

El revisor verifica:

- [ ] Nomenclatura correcta
- [ ] Documentación adecuada
- [ ] Tests añadidos/actualizados
- [ ] Sin código duplicado
- [ ] Manejo de errores apropiado
- [ ] Quality Gate PASSED

---

## 📚 Referencias

- [PEP 8 - Style Guide for Python Code](https://pep8.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [SonarQube Python Rules](https://rules.sonarsource.com/python/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

## ✅ Checklist Rápido

Antes de cada commit, verifica:

- [ ] ✅ Código formateado (100 caracteres máximo)
- [ ] ✅ Nombres siguen convenciones (snake_case, PascalCase)
- [ ] ✅ Funciones < 50 líneas
- [ ] ✅ Complejidad ciclomática < 10
- [ ] ✅ Docstrings en funciones públicas
- [ ] ✅ Imports ordenados alfabéticamente
- [ ] ✅ Sin imports no usados
- [ ] ✅ Excepciones específicas con contexto
- [ ] ✅ Tests añadidos/actualizados
- [ ] ✅ Sin secretos hardcoded
- [ ] ✅ Linting pasa (0 errores)
- [ ] ✅ Tests pasan (100%)
- [ ] ✅ Cobertura ≥ 80%

---

**Versión:** 1.0.0  
**Última actualización:** Noviembre 2025  
**Mantenido por:** Equipo TaskManagerAPI
