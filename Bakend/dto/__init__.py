"""
DTOs (Data Transfer Objects).
Validación y normalización de datos de entrada.
"""
from dto.service_dto import ServiceDTO, ServiceCreateDTO, ServiceReadDTO
from dto.appointment_dto import AppointmentCreateDTO, AppointmentReadDTO, AppointmentDTO
from dto.payment_dto import PaymentDTO
from dto.Interface import BaseDTO, ConvertDTO

__all__ = ["ServiceDTO", "ServiceCreateDTO", "ServiceReadDTO",
            "AppointmentDTO", "AppointmentCreateDTO", "AppointmentReadDTO",
            "PaymentDTO",
             "BaseDTO", "ConvertDTO"]
