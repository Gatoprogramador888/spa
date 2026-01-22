from datetime import timezone
from sqlalchemy import Column, Integer, String, Text, DateTime
from config.database import Base


class SmsLog(Base):
    __tablename__ = "sms_logs"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20))
    message = Column(Text)
    status = Column(String(50))
    created_at = Column(DateTime, default=timezone.utc)
