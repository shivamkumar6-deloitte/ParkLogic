import enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

#Enums for the records purpose
class ParkingPurposeEnum(str, enum.Enum):
    booking = "booking"
    maintenance = "maintenance"



class ParkingRecordBase(BaseModel):
    user_id: int
    spot_id: int
    purpose: ParkingPurposeEnum = ParkingPurposeEnum.booking

class ParkingRecordCreate(ParkingRecordBase):
    pass

class ParkingRecordOut(ParkingRecordBase):
    id: int
    entry_time: datetime
    exit_time: Optional[datetime]

    class Config:
        orm_mode = True