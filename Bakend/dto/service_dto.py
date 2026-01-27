"""
DTO para Service (Servicio).
Valida y normaliza datos de entrada para servicios del spa.
"""
from dto.Interface import BaseDTO, ConvertDTO
from datetime import datetime

class ServiceDTO(BaseDTO):
    id: int
    public_code: str
    name: str
    cost_cents: int
    active: bool = True
    created_at: datetime
    pass

class ServiceCreateDTO(ConvertDTO):
    """
    Data Transfer Object para servicio.
    
    Valida:
    - public_code: no vacío, string, único
    - name: no vacío, string (máx 100 caracteres)
    - cost_cents: entero no negativo
    - active: booleano (opcional, default True)
    """

    def __init__(self, public_code: str, name: str, cost_cents: int, active: bool = True):
        self.public_code = self._validate_public_code(public_code)
        self.name = self._validate_name(name)
        self.cost_cents = self._validate_cost_cents(cost_cents)
        self.active = active

    @classmethod
    def constructo2(cls, service_dto: ServiceDTO):
        """Crear desde ServiceDTO (pasa por validaciones del __init__)"""
        return cls(
            public_code=service_dto.public_code,
            name=service_dto.name,
            cost_cents=service_dto.cost_cents,
            active=service_dto.active
        )

    @staticmethod
    def _validate_public_code(public_code: str) -> str:
        """Valida que public_code no esté vacío y no supere 50 caracteres."""
        if not isinstance(public_code, str) or not public_code.strip():
            raise ValueError("El código público del servicio es requerido.")
        if len(public_code.strip()) > 50:
            raise ValueError("El código público no puede exceder 50 caracteres.")
        return public_code.strip()

    @staticmethod
    def _validate_name(name: str) -> str:
        """Valida que name no esté vacío y no supere 100 caracteres."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre del servicio es requerido.")
        if len(name.strip()) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres.")
        return name.strip()

    @staticmethod
    def _validate_cost_cents(cost_cents: int) -> int:
        """Valida que cost_cents sea un entero no negativo."""
        if not isinstance(cost_cents, int) or cost_cents < 0:
            raise ValueError("El costo debe ser un entero no negativo.")
        return cost_cents
    
    def to_BaseDTO(self) -> ServiceDTO:
        return ServiceDTO(
            id=None,
            public_code=self.public_code,
            name=self.name,
            cost_cents=self.cost_cents,
            active=self.active,
            created_at=None,
        )


class ServiceReadDTO(ConvertDTO):
    """
    Data Transfer Object para lectura de servicio.
    
    Incluye todos los campos de BaseServiceDTO.
    """

    def __init__(self, service_dto: ServiceDTO):
        self.id = service_dto.id
        self.public_code = service_dto.public_code
        self.name = service_dto.name
        self.cost_cents = service_dto.cost_cents
        self.active = service_dto.active
        self.created_at = service_dto.created_at

    @classmethod
    def constructor2(cls,
    id: int,
    public_code: str,
    name: str,
    cost_cents: int,
    active: bool,
    created_at: datetime,
    ):
        return cls(
        id=id,
        public_code=public_code,
        name=name,
        cost_cents=cost_cents,
        active=active,
        created_at=created_at
        )

    def to_BaseDTO(self) -> ServiceDTO:
        return ServiceDTO(
            id=self.id,
            public_code=self.public_code,
            name=self.name,
            cost_cents=self.cost_cents,
            active=self.active,
            created_at=self.created_at,
        )