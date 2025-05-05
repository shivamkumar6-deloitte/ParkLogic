from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..database import Base

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    feedback_type = Column(String)  # 'service', 'lot', 'spot'
    parking_lot_id = Column(Integer, ForeignKey("parking_lot.id"), nullable=True)
    spot_id = Column(Integer, ForeignKey("spot.id"), nullable=True)
    rating = Column(Integer)
    comment = Column(Text)
    created_at =Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="feedbacks")
    parking_lot = relationship("ParkingLot", back_populates="feedbacks")
    spot = relationship("Spot", back_populates="feedbacks")