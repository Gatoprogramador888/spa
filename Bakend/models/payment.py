from datetime import timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from config.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    amount_cents = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, default="PENDING")
    provider_payment_id = Column(String(255))
    created_at = Column(DateTime, default=func.now())

    appointment = relationship("Appointment")
