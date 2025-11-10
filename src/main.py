"""
Punto de entrada de la aplicación Task Manager.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router as task_router
from .config import settings
from .utils.logger import get_logger, setup_logging

# Configurar logging
setup_logging()
logger = get_logger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API REST para gestión de tareas con arquitectura robusta",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(task_router, prefix=settings.API_PREFIX)


@app.get("/", tags=["root"])
async def root():
    """Endpoint raíz de la API."""
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Endpoint de verificación de salud."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.on_event("startup")
async def startup_event():
    """Evento ejecutado al iniciar la aplicación."""
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Documentación disponible en: http://{settings.API_HOST}:{settings.API_PORT}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento ejecutado al cerrar la aplicación."""
    logger.info(f"Cerrando {settings.APP_NAME}")


def main():
    """Función principal para ejecutar la aplicación."""
    import uvicorn

    logger.info(f"Iniciando servidor en {settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()
