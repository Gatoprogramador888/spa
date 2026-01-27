"""
DTO para Payment (Pago).
Valida y normaliza datos de entrada para pagos.
"""
from dto.Interface import BaseDTO, ConvertDTO

class PaymentDTO(BaseDTO):
    """
    Data Transfer Object para pago.
    """

    def __init__(
        self,
        id: int,
        appointment_id: int,
        amount_cents: int,
        status: str,
        provider_payment_id: str = None,
        created_at: str = None,
    ):
        self.id = id
        self.appointment_id = appointment_id
        self.amount_cents = amount_cents
        self.status = status
        self.provider_payment_id = provider_payment_id
        self.created_at = created_at


class PaymentCreateDTO(ConvertDTO):
    """
    Data Transfer Object para pago.
    
    Valida:
    - appointment_id: entero positivo
    - amount_cents: entero positivo
    - status: uno de PENDING, PAID, FAILED (opcional, default PENDING)
    - provider: string opcional (ej. MercadoPago)
    - provider_payment_id: string opcional
    """

    VALID_STATUSES = {"PENDING", "PAID", "FAILED"}

    def __init__(
        self,
        appointment_id: int,
        amount_cents: int,
        status: str = "PENDING",
        provider_payment_id: str = None,
    ):
        self.appointment_id = self._validate_appointment_id(appointment_id)
        self.amount_cents = self._validate_amount_cents(amount_cents)
        self.status = self._validate_status(status)
        self.provider_payment_id = (
            provider_payment_id.strip()
            if isinstance(provider_payment_id, str)
            else provider_payment_id
        )

    @staticmethod
    def _validate_appointment_id(appointment_id: int) -> int:
        """Valida que appointment_id sea un entero positivo."""
        if not isinstance(appointment_id, int) or appointment_id <= 0:
            raise ValueError("El ID de la cita debe ser un entero positivo.")
        return appointment_id

    @staticmethod
    def _validate_amount_cents(amount_cents: int) -> int:
        """Valida que amount_cents sea un entero positivo."""
        if not isinstance(amount_cents, int) or amount_cents < 0:
            raise ValueError("El monto debe ser un entero no negativo.")
        return amount_cents

    def _validate_status(self, status: str) -> str:
        """Valida que status sea un valor válido."""
        if status not in self.VALID_STATUSES:
            valid = ", ".join(self.VALID_STATUSES)
            raise ValueError(f"El estado debe ser uno de: {valid}")
        return status
    
    def to_BaseDTO(self) -> PaymentDTO:
        """
        Convierte el DTO de creación a un DTO base.
        """
        return PaymentDTO(
            id=None,
            appointment_id=self.appointment_id,
            amount_cents=self.amount_cents,
            status=self.status,
            provider_payment_id=self.provider_payment_id,
            created_at=None,
        )
    
class PaymentReadDTO(ConvertDTO):
    """
    Data Transfer Object para leer pago.
    """

    def __init__(
        self,
        id: int,
        appointment_id: int,
        amount_cents: int,
        status: str,
        provider_payment_id: str = None,
        created_at: str = None,
    ):
        self.id = id
        self.appointment_id = appointment_id
        self.amount_cents = amount_cents
        self.status = status
        self.provider_payment_id = provider_payment_id
        self.created_at = created_at

    def to_BaseDTO(self) -> PaymentDTO:
        """
        Convierte el DTO de lectura a un DTO base.
        """
        return PaymentDTO(
            id=self.id,
            appointment_id=self.appointment_id,
            amount_cents=self.amount_cents,
            status=self.status,
            provider_payment_id=self.provider_payment_id,
            created_at=self.created_at,
        )