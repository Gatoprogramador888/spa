from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from config.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    public_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    cost_cents = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
