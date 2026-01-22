"""
Health check endpoint.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("")
def health_check():
    """
    Endpoint de salud de la aplicación.
    """
    return {"status": "ok"}

