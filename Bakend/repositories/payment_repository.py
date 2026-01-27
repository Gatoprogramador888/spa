"""
Repository para Payment (Pago).
Capa de acceso a datos para pagos.
"""

from models.payment import Payment
from config.database import get_db

class PaymentRepository:
    """
    Repository para gestionar pagos en la base de datos.
    """

    def create_payment(self, payment : Payment) -> None:
        """
        Crea un nuevo pago en la base de datos.
        """
        with get_db() as db:
            db.add(payment)
            db.commit()
        
