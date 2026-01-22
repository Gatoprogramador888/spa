"""
DTO para Service (Servicio).
Valida y normaliza datos de entrada para servicios del spa.
"""


class ServiceDTO:
    """
    Data Transfer Object para servicio.
    
    Valida:
    - name: no vacío, string
    - price_cents: entero positivo
    - active: booleano (opcional, default True)
    """

    def __init__(self, name: str, price_cents: int, active: bool = True):
        self.name = self._validate_name(name)
        self.price_cents = self._validate_price_cents(price_cents)
        self.active = active

    @staticmethod
    def _validate_name(name: str) -> str:
        """Valida que name no esté vacío."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre del servicio es requerido y debe ser texto.")
        return name.strip()

    @staticmethod
    def _validate_price_cents(price_cents: int) -> int:
        """Valida que price_cents sea positivo."""
        if not isinstance(price_cents, int) or price_cents < 0:
            raise ValueError("El precio debe ser un entero no negativo.")
        return price_cents
