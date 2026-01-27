"""
DTO para Appointment (Cita).
Valida y normaliza datos de entrada para citas.
"""
from datetime import datetime
from dto.Interface import BaseDTO, ConvertDTO
from typing import ClassVar
from pydantic import field_validator


class AppointmentDTO(BaseDTO):
    """
    Data Transfer Object base para cita.
    
    Valida:
    - customer_name: no vacío, string
    - customer_phone: no vacío, string
    - appointment_date: datetime válido en el futuro
    - service_id: entero positivo
    - status: uno de PENDING, CONFIRMED, CANCELLED (opcional, default PENDING)
    """

    VALID_STATUSES : ClassVar[set[str]] = {"PENDING", "CONFIRMED", "CANCELLED"}

    customer_name: str
    customer_phone: str
    appointment_date: datetime
    service_id: str # ID del servicio asociado pero el publico es str
    status: str = "PENDING"
    created_at: datetime
    total_cost_cents: int = 0
    deposit_paid_cents: int = 0
    remaining_cents: int = 0
    id : int = 0

    @field_validator('status')
    @classmethod
    def validate_status(cls, status: str) -> str:
        """Valida que status sea un valor válido."""
        if status not in cls.VALID_STATUSES:
            valid = ", ".join(cls.VALID_STATUSES)
            raise ValueError(f"El estado debe ser uno de: {valid}")
        return status

class AppointmentCreateDTO(ConvertDTO):
    """
    Data Transfer Object para cita.
    """

    VALID_STATUSES = {"PENDING", "CONFIRMED", "CANCELLED"}

    def __init__(
            self,
            customer_name: str,
            customer_phone: str,
            appointment_date: datetime,
            service_id: str,
            status: str = "PENDING"
    ):
        self.customer_name = self._validate_customer_name(customer_name)
        self.customer_phone = self._validate_customer_phone(customer_phone)
        self.appointment_date = self._validate_appointment_date(appointment_date)
        self.service_id = self._validate_service_id(service_id)
        self.status = self._validate_status(status)

    @classmethod
    def Constructor2(cls, appointment_dto : AppointmentDTO):
        return cls(
                customer_name=appointment_dto.customer_name,
                customer_phone=appointment_dto.customer_phone,
                appointment_date=appointment_dto.appointment_date,
                service_id=appointment_dto.service_id,
                status=appointment_dto.status
        )

    @staticmethod
    def _validate_customer_name(name: str) -> str:
        """Valida que customer_name no esté vacío."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre del cliente es requerido.")
        return name.strip()

    @staticmethod
    def _validate_customer_phone(phone: str) -> str:
        """Valida que customer_phone no esté vacío."""
        if not isinstance(phone, str) or not phone.strip():
            raise ValueError("El teléfono del cliente es requerido.")
        return phone.strip()

    @staticmethod
    def _validate_appointment_date(dt: datetime) -> datetime:
        """Valida que appointment_date sea un datetime válido."""
        if not isinstance(dt, datetime):
            raise ValueError("La fecha y hora de la cita debe ser un datetime válido.")
        return dt

    @staticmethod
    def _validate_service_id(service_id: str) -> str:
        """Valida que service_id sea un entero positivo."""
        if not isinstance(service_id, str) or len(service_id) <= 0:
            raise ValueError("El ID del servicio debe ser un str no vacio.")
        return service_id

    def _validate_status(self, status: str) -> str:
        """Valida que status sea un valor válido."""
        if status not in self.VALID_STATUSES:
            valid = ", ".join(self.VALID_STATUSES)
            raise ValueError(f"El estado debe ser uno de: {valid}")
        return status
    
    def to_BaseDTO(self) -> AppointmentDTO:
        return AppointmentDTO(
            customer_name=self.customer_name,
            customer_phone=self.customer_phone,
            appointment_date=self.appointment_date,
            service_id=self.service_id,
            status=self.status,
            created_at=datetime.now()
        )

class AppointmentReadDTO(ConvertDTO):
    
    def __init__(self, appointment_dto: AppointmentDTO):
        self.id = appointment_dto.id
        self.customer_name = appointment_dto.customer_name
        self.customer_phone = appointment_dto.customer_phone
        self.appointment_date = appointment_dto.appointment_date
        self.status = appointment_dto.status
        self.service_id = appointment_dto.service_id
        self.created_at = appointment_dto.created_at
        self.total_cost_cents = appointment_dto.total_cost_cents
        self.deposit_paid_cents = appointment_dto.deposit_paid_cents
        self.remaining_cents = appointment_dto.remaining_cents

    @classmethod
    def constructor2(
        cls,
        id: int,
        customer_name: str,
        customer_phone: str,
        appointment_date: datetime,
        status: str,
        service_id: str,
        created_at: datetime,
        total_cost_cents: int = 0,
        deposit_paid_cents: int = 0,
        remaining_cents: int = 0
    ):
        obj = cls.__new__(cls)
        obj.id = id
        obj.customer_name = customer_name
        obj.customer_phone = customer_phone
        obj.appointment_date = appointment_date
        obj.status = status
        obj.service_id = service_id
        obj.created_at = created_at
        obj.total_cost_cents = total_cost_cents
        obj.deposit_paid_cents = deposit_paid_cents
        obj.remaining_cents = remaining_cents
        return obj

    @classmethod
    def constructor3(cls, appointment_dto : AppointmentReadDTO):
        obj = cls.__new__(cls)
        obj.id = appointment_dto.id
        obj.customer_name = appointment_dto.customer_name
        obj.customer_phone = appointment_dto.customer_phone
        obj.appointment_date = appointment_dto.appointment_date
        obj.status = appointment_dto.status
        obj.service_id = appointment_dto.service_id
        obj.created_at = appointment_dto.created_at
        obj.total_cost_cents = appointment_dto.total_cost_cents
        obj.deposit_paid_cents = appointment_dto.deposit_paid_cents
        obj.remaining_cents = appointment_dto.remaining_cents
        return obj

    def to_BaseDTO(self) -> AppointmentDTO:
        return AppointmentDTO(
            customer_name=self.customer_name,
            customer_phone=self.customer_phone,
            appointment_date=self.appointment_date,
            status=self.status,
            service_id=self.service_id,
            created_at=self.created_at
        )