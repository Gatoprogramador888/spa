"""
Database configuration and session factory.
Configuración segura de base de datos usando variables de entorno.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from contextlib import contextmanager

# Cargar variables de entorno
load_dotenv()

# Base para todos los modelos
Base = declarative_base()

# URL de base de datos desde variable de entorno .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

print(f"Using database URL: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    """
    Dependency para obtener sesión de base de datos.
    TODO: Implementar inyección de dependencias real
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Commit automático si todo sale bien
    except Exception as e:
        db.rollback()  # Rollback automático en caso de error
        print(f"Database session error: {e}")
        raise  # Re-lanza la excepción
    finally:
        db.close()


def init_db():
    """
    Inicializa todas las tablas en la base de datos.
    TODO: Usar Flask-Migrate en producción
    """
    Base.metadata.create_all(bind=engine)
