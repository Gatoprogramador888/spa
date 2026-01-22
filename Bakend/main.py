"""
FastAPI application entry point.
Main application configuration and router registration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config

# Importar routers
from api.health import router as health_router
from api.appointments import router as appointments_router
from api.payments import router as payments_router
from api.chat import router as chat_router
from api.login import router as login_router
from api.services import router as services_router
from api.chat_ws import router as chat_ws_router


def create_app():
    """
    Factory pattern para crear la aplicación FastAPI.
    Carga configuración desde variables de entorno.
    """
    app = FastAPI(
        title="SPA API",
        description="API para gestión de citas, pagos y chat",
        version="1.0.0"
    )

    # Configuración CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Importar y inicializar base de datos (lazy import)
    try:
        from config.database import init_db
        init_db()
    except Exception as e:
        print(f"Advertencia: No se pudo inicializar la BD: {e}")

    # Registrar routers
    app.include_router(health_router)
    app.include_router(appointments_router)
    app.include_router(payments_router)
    app.include_router(chat_router)
    app.include_router(login_router)
    app.include_router(services_router)
    app.include_router(chat_ws_router)

    # TODO: Configurar error handlers personalizados
    # TODO: Agregar logging

    return app


if __name__ == '__main__':
    import uvicorn
    app = create_app()
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT
    )
