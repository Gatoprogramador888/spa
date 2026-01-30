"""
Domain para Payment (Pago).
Lógica de negocio relacionada con pagos.
"""
pass

from dto.payment_dto import PaymentCreateDTO, PaymentReadDTO, PaymentDTO  
from repositories.payment_repository import PaymentRepository  
from models.payment import Payment  
from datetime import datetime
from dto.appointment_dto import AppointmentCreateDTO, AppointmentDTO  
from dto.service_dto import ServiceDTO  

class IDiscountPayment():
    _discunt_rate : float
    def __init__(self, discount_rate : float):
        self._discunt_rate = discount_rate

    def cost_discounted(self, amount_cents : int) -> int:  
        pass
    
    def apply_discount(self, amount_cents : int) -> int:
        pass


class IAdvancePayment():
    _advance_rate : float
    def __init__(self, advance_rate : float):
        self._advance_rate = advance_rate

    def cost_advance(self, amount_cents : int) -> int: 
        pass

    def apply_advance(self, amount_cents : int) -> int:
        pass

class IProcessPayment():
    def __init__(self):
        pass
    def process_payment(
                        discount : IDiscountPayment,
                        advance : IAdvancePayment,
                        cent: int) -> int:
        pass

def discount_and_advance_payment_allocation_for_appointment(
                                 appointment_dto : AppointmentCreateDTO,
                                 service_dto : ServiceDTO,
                                 discount : IDiscountPayment,
                                 advance : IAdvancePayment) -> None:
    """
    Lógica para obtener el costo en centavos de un servicio.
    """
    service_cost_cents = service_dto.cost_cents
    advance_amount = advance.cost_advance(service_cost_cents)
    discounted_amount = discount.cost_discounted(service_cost_cents)
    appointment_dto.cost_cents = service_dto.cost_cents
    appointment_dto.advance_cents = advance_amount
    appointment_dto.discount_cents = discounted_amount


def process_payment(
                                 appointment_dto : AppointmentDTO,
                                 service_dto : ServiceDTO,
                                 discount : IDiscountPayment,
                                 advance : IAdvancePayment,
                                 process : IProcessPayment,
                                 payment_repository : PaymentRepository) -> bool:
    """
    Lógica para procesar el pago de una cita.
    """
    
    service_cost_cents = service_dto.cost_cents
    total_payment_cents = process.process_payment(discount, advance, service_cost_cents)

    """Enviar a registrar el pago al punto de venta tambien obtener el id del pago
    para en un futuro actualizar el estado del pago segun la respuesta del proveedor
    y ver si se cancela o no la cita y el pago"""

    #delay por mientras para disimular la logica

    payment = PaymentDTO(
        id = 0,
        appointment_id = appointment_dto.id,
        amount_cents = total_payment_cents,
        status = "PENDING",
        provider_payment_id = None,
        created_at = datetime.now().isoformat(),
        )
    "Aqui se registra el pago en la base de datos"
    payment_model = Payment(**payment.model_dump(exclude={'id', 'created_at'}))
    payment_repository.create_payment(payment_model)
    return False