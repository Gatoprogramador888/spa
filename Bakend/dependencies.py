from repositories.appointment_repository import AppointmentRepository

def get_appointments() -> AppointmentRepository:
    return AppointmentRepository()