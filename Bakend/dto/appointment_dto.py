"""
DTO para Appointment (Cita).
Valida y normaliza datos de entrada para citas.
"""
from datetime import datetime


class AppointmentCreateDTO:
    """
    Data Transfer Object para cita.
    
    Valida:
    - customer_name: no vacío, string
    - customer_phone: no vacío, string
    - appointment_datetime: datetime válido en el futuro
    - service_id: entero positivo
    - status: uno de PENDING, CONFIRMED, CANCELLED (opcional, default PENDING)
    """

    VALID_STATUSES = {"PENDING", "CONFIRMED", "CANCELLED"}

    def __init__(
        self,
        customer_name: str,
        customer_phone: str,
        appointment_datetime: datetime,
        service_id: int,
        status: str = "PENDING",
    ):
        self.customer_name = self._validate_customer_name(customer_name)
        self.customer_phone = self._validate_customer_phone(customer_phone)
        self.appointment_datetime = self._validate_appointment_datetime(
            appointment_datetime
        )
        self.service_id = self._validate_service_id(service_id)
        self.status = self._validate_status(status)

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
    def _validate_appointment_datetime(dt: datetime) -> datetime:
        """Valida que appointment_datetime sea un datetime válido."""
        if not isinstance(dt, datetime):
            raise ValueError("La fecha y hora de la cita debe ser un datetime válido.")
        return dt

    @staticmethod
    def _validate_service_id(service_id: int) -> int:
        """Valida que service_id sea un entero positivo."""
        if not isinstance(service_id, int) or service_id <= 0:
            raise ValueError("El ID del servicio debe ser un entero positivo.")
        return service_id

    def _validate_status(self, status: str) -> str:
        """Valida que status sea un valor válido."""
        if status not in self.VALID_STATUSES:
            valid = ", ".join(self.VALID_STATUSES)
            raise ValueError(f"El estado debe ser uno de: {valid}")
        return status

class AppointmentReadDTO:
    def __init__(
        self,
        id: int,
        customer_name: str,
        customer_phone: str,
        appointment_datetime: datetime,
        status: str,
        service_id: int,
        created_at: datetime,
    ):
        self.id = id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.appointment_datetime = appointment_datetime
        self.status = status
        self.service_id = service_id
        self.created_at = created_at

    