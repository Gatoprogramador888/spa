"""
Appointments API endpoints.
TODO: Implementar lógica de citas
"""
from flask import Blueprint, jsonify, request

appointments_bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')


# TODO: Implementar GET /api/appointments
@appointments_bp.route('', methods=['GET'])
def get_appointments():
    """
    TODO: Obtener todas las citas
    """
    pass


# TODO: Implementar POST /api/appointments
@appointments_bp.route('', methods=['POST'])
def create_appointment():
    """
    TODO: Crear nueva cita
    TODO: Validar con DTO
    TODO: Llamar a servicio de negocio
    """
    pass


# TODO: Implementar GET /api/appointments/<id>
@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """
    TODO: Obtener cita por ID
    """
    pass


# TODO: Implementar PUT /api/appointments/<id>
@appointments_bp.route('/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """
    TODO: Actualizar cita
    """
    pass


# TODO: Implementar DELETE /api/appointments/<id>
@appointments_bp.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """
    TODO: Eliminar cita
    """
    pass
