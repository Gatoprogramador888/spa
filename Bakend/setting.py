"""
Configuración de la aplicación.
Variables de entorno y configuraciones globales.
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class Config:
    """Configuración base para la aplicación."""
    
    # Base de datos
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./app.db"  # Default para desarrollo local
    )
    
    # Flask
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    
    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-change-me")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    # API
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", "5000"))
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


config = Config()
