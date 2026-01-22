"""
DTOs (Data Transfer Objects).
Validación y normalización de datos de entrada.
"""
from dto.service_dto import ServiceDTO
from dto.appointment_dto import AppointmentDTO
from dto.payment_dto import PaymentDTO

__all__ = ["ServiceDTO", "AppointmentDTO", "PaymentDTO"]
