import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database import Base

class UserRoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"
    attendant = "attendant"

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    vehicle_number = Column(String)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.user, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    parking_records = relationship("ParkingRecord", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")