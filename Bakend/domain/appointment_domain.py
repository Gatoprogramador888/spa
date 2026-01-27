"""
Domain para Appointment (Cita).
Lógica de negocio relacionada con citas.
"""
from dto.appointment_dto import AppointmentCreateDTO, AppointmentReadDTO, AppointmentDTO
from utils.datetime_utils import is_future_date, Datetime_to_Date_and_Date
from utils.phone_utils import is_valid_phone_number
from repositories.appointment_repository import AppointmentRepository
from repositories.service_repository import ServiceRepository
from repositories.payment_repository import PaymentRepository
from models.appointment import Appointment
from models.service import Service
from datetime import datetime
from domain.service_domain import get_service_by_public_id
from domain.payment_domain import IDiscountPayment, IAdvancePayment, IProcessPayment, process_payment, discount_and_advance_payment_allocation_for_appointment


#Validar si existe dicha cita y servicio pero en service_domain.py

"""AGREGAR LA LOGICA PARA OBTENER LOS COSTOS DE LA CITA SEGUN EL SERVICIO"""
def schedule_appointment(appointment_data : AppointmentCreateDTO,
                          appointmenReposity :AppointmentRepository,
                          serviceReposity : ServiceRepository,
                          paymentReposity : PaymentRepository) -> bool:
    """
    Lógica para programar una nueva cita.
    """
    is_future = is_future_date(appointment_data.appointment_date) 
    is_valid_phone = is_valid_phone_number(appointment_data.customer_phone)
    service_exists = get_service_by_public_id(appointment_data.service_id,  
                                                serviceReposity)
    result = is_future and is_valid_phone and service_exists is not None
    if result:
        discount = IDiscountPayment(0.1),  # Ejemplo: 10% de descuento de ejemplo
        advance = IAdvancePayment(0.2)    # Ejemplo: 20% de pago adelantado de ejemplo
        discount_and_advance_payment_allocation_for_appointment(
            appointment_data,
            service_exists,
            discount,
            advance
            )
        # Lógica para programar la cita
        appointmen = Appointment(**appointment_data.to_BaseDTO().model_dump(exclude={'created_at'}))
        appointmen.service_id = service_exists.id
        appointmen.total_cost_cents = service_exists.cost_cents
        appointmenReposity.create_appointment(appointmen)
        appointment_dto = AppointmentDTO(
        **appointmen.__dict__,
        service_name=appointmen.service.name,
        service_public_code=appointmen.service.public_code
    )
        process_payment(appointment_dto,
                        service_exists,
                        discount,
                        advance,
                        IProcessPayment(),
                        paymentReposity)
        return True
    return False

def get_appointment_by_number(number : str,
                                       appointmenReposity : AppointmentRepository) -> list[AppointmentDTO]:
    """
    Lógica para obtener una cita por número de teléfono.
    """
    appointments = appointmenReposity.get_appointment_by_number(number)

    appointmenReturn = []

    for appointment in appointments:
        appointmenReturn.append(appointment.to_BaseDTO())

    return appointmenReturn


def get_appointment_by_date(date : datetime,
                                       appointmenReposity : AppointmentRepository) -> list[AppointmentDTO]:
    """
    Lógica para obtener una cita por fecha .
    """
    dateStart, dateEnd = Datetime_to_Date_and_Date(date)
    appointments = appointmenReposity.get_appointment_by_date(dateStart, dateEnd)
    appointmentsReturn = []
    for appointment in appointments:
        appointmentsReturn.append(appointment.to_BaseDTO())
    return appointmentsReturn