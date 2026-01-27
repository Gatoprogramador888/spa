"""
Appointments API endpoints.
TODO: Implementar lógica de citas
"""
from fastapi import APIRouter, Query, Header, HTTPException, Depends
from typing import Optional
from domain.appointment_domain import schedule_appointment, get_appointment_by_number, get_appointment_by_date
from repositories.appointment_repository import AppointmentRepository
from repositories.service_repository import ServiceRepository
from dto.appointment_dto import AppointmentDTO, AppointmentCreateDTO
from dependencies import get_appointments, get_service
from datetime import datetime

router = APIRouter(prefix="/api/appointments", tags=["appointments"])

# TODO: Implementar GET /api/appointments/private
# Pedir autenticación especial para el spa
@router.get("/private", response_model=list[AppointmentDTO])
def get_appointments_private(authorization: Optional[str] = Header(None),
                             appointment_repo: AppointmentRepository = Depends(get_appointments)):
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
    
    appointments = get_appointment_by_date(datetime.now(), appointment_repo)

    return appointments


# TODO: Implementar POST /api/appointments
@router.post("/create", status_code=201)
def create_appointment(appointment_data: AppointmentDTO,
                       appointment_repo: AppointmentRepository = Depends(get_appointments),
                       service_repo: ServiceRepository = Depends(get_service)):
    """
    TODO: Crear nueva cita
    TODO: Validar con DTO
    TODO: Llamar a servicio de negocio
    """
    appointment = AppointmentCreateDTO.Constructor2(appointment_data)
    success = schedule_appointment(appointment, appointment_repo, service_repo)
    if not success:
        raise HTTPException(status_code=400, detail="Datos de cita inválidos")
    return {"message": "Cita creada exitosamente"}


# TODO: Implementar GET /api/appointments
@router.get("/appointments", response_model=list[AppointmentDTO])
def get_appointments(phone_number: str = Query(..., description="Número de teléfono del usuario"),
                     appointment_repo: AppointmentRepository = Depends(get_appointments)):
    """
    TODO: Obtener todas las citas del usuario por numero de teléfono
    """
    if not phone_number:
        raise HTTPException(status_code=400, detail="phone_number es requerido")
    # Retornar citas del usuario
    appointments = get_appointment_by_number(phone_number, appointment_repo)
    return appointments

"""
        ESTOS METODOS YA NO SON NECESARIOS POR AHORA
"""
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
