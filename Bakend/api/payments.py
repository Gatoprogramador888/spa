"""
Payments API endpoints.
TODO: Implementar lógica de pagos
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/payments", tags=["payments"])


# TODO: Implementar GET /api/payments
@router.get("")
def get_payments():
    """
    TODO: Obtener todos los pagos
    """
    pass


# TODO: Implementar POST /api/payments
@router.post("")
def create_payment():
    """
    TODO: Crear nuevo pago
    TODO: Validar con DTO
    TODO: Llamar a servicio de negocio
    """
    pass


# TODO: Implementar GET /api/payments/<id>
@router.get("/{payment_id}")
def get_payment(payment_id: int):
    """
    TODO: Obtener pago por ID
    """
    pass


# TODO: Implementar PUT /api/payments/<id>
@router.put("/{payment_id}")
def update_payment(payment_id: int):
    """
    TODO: Actualizar pago
    """
    pass


# TODO: Implementar DELETE /api/payments/<id>
@router.delete("/{payment_id}")
def delete_payment(payment_id: int):
    """
    TODO: Eliminar pago
    """
    pass
