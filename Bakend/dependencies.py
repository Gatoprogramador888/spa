from repositories.appointment_repository import AppointmentRepository
from repositories.service_repository import ServiceRepository

def get_appointments() -> AppointmentRepository:
    return AppointmentRepository()

def get_service() -> ServiceRepository:
    return ServiceRepository()