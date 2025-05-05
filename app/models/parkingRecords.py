import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..database import Base

class ParkingPurposeEnum(str, enum.Enum):
    booking = "booking"
    maintenance = "maintenance"

class ParkingRecords(Base):
    __tablename__ = "parking_record"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    spot_id = Column(Integer, ForeignKey("spot.id"))
    entry_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    exit_time = Column(DateTime, nullable=True)
    purpose = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="parking_records")
    spot = relationship("Spot", back_populates="parking_records")