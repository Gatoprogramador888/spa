"""
Repository para Appointment (Cita).
Capa de acceso a datos para citas.
"""
from models.appointment import Appointment
from models.service import Service
from dto.appointment_dto import AppointmentCreateDTO, AppointmentReadDTO
from config.database import get_db
from datetime import date

class AppointmentRepository:
    """
    Repository para gestionar citas en la base de datos.
    """
    def __init__(self):
        pass

    def get_appointment_by_number(self, number : str) -> list[AppointmentReadDTO]:
        with get_db() as conn:
            try:
                rows = conn.query(Appointment).filter(Appointment.customer_phone == number).all()
                appointments = []
                for row in rows:
                    appointment = Appointment(*row)
                    appointments.append(AppointmentReadDTO(
                        id=appointment.id,
                        customer_name=appointment.customer_name,
                        customer_phone=appointment.customer_phone,
                        appointment_date=appointment.appointment_date,
                        status=appointment.status,
                        service_id=appointment.service_id,
                        created_at=appointment.created_at,))
                return appointments
            except Exception as e:
                #loging error
                raise e


    def get_appointment_by_date(self, dateStart : date, dateEnd) -> list[AppointmentReadDTO]:
        with get_db() as conn:
            try:
                rows = conn.query(Appointment).filter(Appointment.appointment_date >= dateStart,
                                              Appointment.appointment_date < dateEnd).all()
                appointments = []
                for row in rows:
                    appointment = Appointment(*row)
                    appointments.append(AppointmentReadDTO(
                        id=appointment.id,
                        customer_name=appointment.customer_name,
                        customer_phone=appointment.customer_phone,
                        appointment_date=appointment.appointment_date,
                        status=appointment.status,
                        service_id=appointment.service_id,
                        created_at=appointment.created_at,))
                return appointments
            except Exception as e:
                #loging error
                raise e

    def create_appointment(self, appointment_data: Appointment) -> None:
        with get_db() as conn:
            conn.add(appointment_data)
            conn.commit()
