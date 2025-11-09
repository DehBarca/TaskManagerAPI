"""
Gestión de conexión a base de datos.
Para este proyecto usaremos una implementación simple en memoria/archivo.
"""

from typing import Dict, Any
import json
from pathlib import Path
from ..config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class Database:
    """Clase para gestionar la persistencia de datos."""

    def __init__(self):
        """Inicializa la base de datos."""
        self.data: Dict[str, Dict[str, Any]] = {"tasks": {}}
        self.db_file = self._get_db_file()
        self._load_data()

    def _get_db_file(self) -> Path:
        """Obtiene la ruta del archivo de base de datos."""
        db_path = settings.get_database_path()
        if db_path:
            return db_path
        return Path(__file__).parent.parent.parent / "tasks.db.json"

    def _load_data(self):
        """Carga los datos desde el archivo."""
        try:
            if self.db_file.exists():
                with open(self.db_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                logger.info(f"Datos cargados desde {self.db_file}")
            else:
                logger.info("Base de datos inicializada en memoria")
        except Exception as e:
            logger.error(f"Error al cargar datos: {e}")
            self.data = {"tasks": {}}

    def _save_data(self):
        """Guarda los datos en el archivo."""
        try:
            self.db_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
            logger.debug(f"Datos guardados en {self.db_file}")
        except Exception as e:
            logger.error(f"Error al guardar datos: {e}")
            raise

    def get_all(self, collection: str) -> Dict[str, Any]:
        """Obtiene todos los elementos de una colección."""
        return self.data.get(collection, {})

    def get_by_id(self, collection: str, item_id: str) -> Any:
        """Obtiene un elemento por su ID."""
        return self.data.get(collection, {}).get(item_id)

    def insert(self, collection: str, item_id: str, item: Dict[str, Any]):
        """Inserta un nuevo elemento."""
        if collection not in self.data:
            self.data[collection] = {}
        self.data[collection][item_id] = item
        self._save_data()

    def update(self, collection: str, item_id: str, item: Dict[str, Any]):
        """Actualiza un elemento existente."""
        if collection in self.data and item_id in self.data[collection]:
            self.data[collection][item_id] = item
            self._save_data()
            return True
        return False

    def delete(self, collection: str, item_id: str) -> bool:
        """Elimina un elemento."""
        if collection in self.data and item_id in self.data[collection]:
            del self.data[collection][item_id]
            self._save_data()
            return True
        return False

    def clear_collection(self, collection: str):
        """Limpia una colección completa."""
        if collection in self.data:
            self.data[collection] = {}
            self._save_data()


# Instancia singleton de la base de datos
_db_instance = None


def get_database() -> Database:
    """Obtiene la instancia singleton de la base de datos."""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
