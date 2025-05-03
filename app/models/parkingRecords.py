import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class ParkingPurposeEnum(str, enum.Enum):
    booking = "booking"
    maintenance = "maintenance"

class ParkingRecords(Base):
    __tablename__ = "parking_record"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    spot_id = Column(Integer, ForeignKey("spot.id"))
    entry_time = Column(DateTime, default=datetime.now(datetime.UTC))
    exit_time = Column(DateTime, nullable=True)
    purpose = Column(Enum(ParkingPurposeEnum), default=ParkingPurposeEnum.booking)

    user = relationship("User", back_populates="parking_records")
    spot = relationship("Spot", back_populates="parking_records")