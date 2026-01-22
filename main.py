"""
Flask application entry point.
Main application configuration and blueprint registration.
"""
from flask import Flask
from config import config

# Importar blueprints
from api.health import health_bp
from api.appointments import appointments_bp
from api.payments import payments_bp
from api.chat import chat_bp


def create_app():
    """
    Factory pattern para crear la aplicación Flask.
    Carga configuración desde variables de entorno.
    """
    app = Flask(__name__)

    # Configuración desde config.py
    app.config['DEBUG'] = config.DEBUG
    app.config['SECRET_KEY'] = config.SECRET_KEY

    # Importar y inicializar base de datos (lazy import)
    try:
        from config.database import init_db
        init_db()
    except Exception as e:
        print(f"Advertencia: No se pudo inicializar la BD: {e}")

    # Registrar blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(chat_bp)

    # TODO: Registrar error handlers personalizados
    # TODO: Configurar CORS si es necesario
    # TODO: Agregar logging

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=config.API_HOST, port=config.API_PORT, debug=config.DEBUG)
