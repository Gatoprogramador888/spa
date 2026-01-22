"""
Domain para Appointment (Cita).
Lógica de negocio relacionada con citas.
"""
from dto.appointment_dto import AppointmentCreateDTO, AppointmentReadDTO
from utils.datetime_utils import is_future_date, Datetime_to_Date_and_Date
from utils.phone_utils import is_valid_phone_number
from repositories.appointment_repository import AppointmentRepository
from models.appointment import Appointment
from datetime import datetime

#Validar si existe dicha cita y servicio pero en service_domain.py

def schedule_appointment(appointment_data : AppointmentCreateDTO,
                          appointmenReposity : AppointmentRepository) -> bool:
    """
    Lógica para programar una nueva cita.
    """
    if is_future_date(appointment_data.appointment_datetime) and is_valid_phone_number(appointment_data.customer_phone):
        # Lógica para programar la cita
        appointmen = Appointment(
            customer_name=appointment_data.customer_name,
            customer_phone=appointment_data.customer_phone,
            appointment_datetime=appointment_data.appointment_datetime,
            service_id=appointment_data.service_id
        )
        appointmenReposity.create_appointment(appointmen)
        return True
    return False

def get_appointment_by_number(number : str,
                                       appointmenReposity : AppointmentRepository) -> list[AppointmentReadDTO]:
    """
    Lógica para obtener una cita por número de teléfono.
    """
    appointments = appointmenReposity.get_appointment_by_number(number)
    return appointments


def get_appointment_by_date(date : datetime,
                                       appointmenReposity : AppointmentRepository) -> list[AppointmentReadDTO]:
    """
    Lógica para obtener una cita por fecha .
    """
    dateStart, dateEnd = Datetime_to_Date_and_Date(date)
    appointments = appointmenReposity.get_appointment_by_date(dateStart, dateEnd)
    return appointments