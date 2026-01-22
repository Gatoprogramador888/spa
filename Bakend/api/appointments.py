"""
Appointments API endpoints.
TODO: Implementar lógica de citas
"""
from fastapi import APIRouter, Query, Header, HTTPException
from typing import Optional

router = APIRouter(prefix="/api/appointments", tags=["appointments"])


# TODO: Implementar GET /api/appointments
@router.get("")
def get_appointments(phone_number: str = Query(..., description="Número de teléfono del usuario")):
    """
    TODO: Obtener todas las citas del usuario por numero de teléfono
    """
    if not phone_number:
        raise HTTPException(status_code=400, detail="phone_number es requerido")
    # Retornar citas del usuario
    pass


# TODO: Implementar GET /api/appointments/private
# Pedir autenticación especial para el spa
@router.get("/private")
def get_appointments_private(authorization: Optional[str] = Header(None)):
    """
    Obtener todas las citas del día para el spa
    Requiere autenticación JWT
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")
    
    try:
        # El formato es: "Bearer <token>"
        token = authorization.split(' ')[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Formato de Authorization inválido")
    
    # Aquí validarías el token con tu librería JWT
    # import jwt
    # decoded = jwt.decode(token, 'tu_secret_key', algorithms=['HS256'])
    
    return {'appointments': []}


# TODO: Implementar POST /api/appointments
@router.post("")
def create_appointment():
    """
    TODO: Crear nueva cita
    TODO: Validar con DTO
    TODO: Llamar a servicio de negocio
    """
    pass


# TODO: Implementar GET /api/appointments/<id>
@router.get("/{appointment_id}")
def get_appointment(appointment_id: int):
    """
    TODO: Obtener cita por ID
    """
    pass


# TODO: Implementar PUT /api/appointments/<id>
@router.put("/{appointment_id}")
def update_appointment(appointment_id: int):
    """
    TODO: Actualizar cita
    """
    pass


# TODO: Implementar DELETE /api/appointments/<id>
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int):
    """
    TODO: Eliminar cita
    """
    pass
