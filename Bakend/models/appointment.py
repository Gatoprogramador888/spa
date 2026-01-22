from datetime import timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    appointment_datetime = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False, default="PENDING")
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    created_at = Column(DateTime, default=timezone.utc)

    service = relationship("Service")
