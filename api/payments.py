"""
Payments API endpoints.
TODO: Implementar lógica de pagos
"""
from flask import Blueprint, jsonify, request

payments_bp = Blueprint('payments', __name__, url_prefix='/api/payments')


# TODO: Implementar GET /api/payments
@payments_bp.route('', methods=['GET'])
def get_payments():
    """
    TODO: Obtener todos los pagos
    """
    pass


# TODO: Implementar POST /api/payments
@payments_bp.route('', methods=['POST'])
def create_payment():
    """
    TODO: Crear nuevo pago
    TODO: Validar con DTO
    TODO: Llamar a servicio de negocio
    """
    pass


# TODO: Implementar GET /api/payments/<id>
@payments_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    """
    TODO: Obtener pago por ID
    """
    pass


# TODO: Implementar PUT /api/payments/<id>
@payments_bp.route('/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    """
    TODO: Actualizar pago
    """
    pass


# TODO: Implementar DELETE /api/payments/<id>
@payments_bp.route('/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    """
    TODO: Eliminar pago
    """
    pass
