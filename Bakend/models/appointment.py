from datetime import timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from config.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    total_cost_cents = Column(Integer(11), nullable=False)  # ← Nuevo
    deposit_paid_cents = Column(Integer(11), default=0)  # ← Nuevo (opcional)
    remaining_cents = Column(Integer(11), default=0)  # ← Nuevo (opcional)
    status = Column(String(50), default="PENDING")
    created_at = Column(DateTime, server_default=func.now())

    service = relationship("Service", lazy="joined")
