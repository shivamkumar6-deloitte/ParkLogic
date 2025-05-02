
from sqlalchemy import Column, Integer, String, Boolean,  ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class ParkingLot(Base):
    __tablename__ = "parking_lot"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)

    floors = relationship("Floor", back_populates="parking_lot")
    feedbacks = relationship("Feedback", back_populates="parking_lot")

class Floor(Base):
    __tablename__ = "floor"
    id = Column(Integer, primary_key=True, index=True)
    parking_lot_id = Column(Integer, ForeignKey("parking_lot.id"))
    floor_number = Column(Integer)

    parking_lot = relationship("ParkingLot", back_populates="floors")
    spots = relationship("Spot", back_populates="floor")


class Spot(Base):
    __tablename__ = "spot"
    id = Column(Integer, primary_key=True, index=True)
    floor_id = Column(Integer, ForeignKey("floor.id"))
    spot_number = Column(String)
    is_occupied = Column(Boolean, default=False)

    floor = relationship("Floor", back_populates="spots")
    parking_records = relationship("ParkingRecord", back_populates="spot")
    feedbacks = relationship("Feedback", back_populates="spot")
