from pydantic import BaseModel

# --- Parking Lot Schemas ---

class ParkingLotCreate(BaseModel):
    name: str
    address: str

class ParkingLotOut(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        orm_mode = True

# --- Floor Schemas ---

class FloorCreate(BaseModel):
    parking_lot_id: int
    floor_number: int

class FloorOut(BaseModel):
    id: int
    parking_lot_id: int
    floor_number: int

    class Config:
        orm_mode = True

# --- Spot Schemas ---

class SpotCreate(BaseModel):
    floor_id: int
    spot_number: str

class SpotOut(BaseModel):
    id: int
    floor_id: int
    spot_number: str
    is_occupied: bool

    class Config:
        orm_mode = True