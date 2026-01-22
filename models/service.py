from datetime import timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from config.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price_cents = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=timezone.utc)
