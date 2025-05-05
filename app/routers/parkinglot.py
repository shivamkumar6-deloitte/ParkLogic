from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Annotated
from sqlalchemy.orm import Session
from app.models.parkinglot import ParkingLot
from app.schemas.parkinglot import ParkingLotCreate, ParkingLotOut
from app.database import SessionLocal
from app.routers.auth import get_current_user

# i changed all the async to normal because i learned that normal SQLAlchemy orm is not async
router = APIRouter(
    prefix="/parkinglot",
    tags=["parkinglot"]
)

#  the db dependency func
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Create a parking lot (admin only)
@router.post("/", response_model=ParkingLotOut, description="Admin only")
def create_parking_lot(
    lot: ParkingLotCreate,
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    db_lot = ParkingLot(name=lot.name, address=lot.address)
    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return db_lot

# List all parking lots (anyone)
@router.get("/", response_model=List[ParkingLotOut], description="All Users allowed")
def get_parking_lots(
    db: db_dependency,
    user: user_dependency
):
    lots = db.query(ParkingLot).all()
    return lots

# Get a parking lot by id (anyone)
@router.get("/{lot_id}", response_model=ParkingLotOut, description="Admin only")
def get_parking_lot(
    lot_id: int,
    db: db_dependency,
    user: user_dependency
):
    lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    return lot

# Update a parking lot (admin only)
@router.put("/{lot_id}", response_model=ParkingLotOut, description="Admin only")
def update_parking_lot(
    lot_id: int,
    lot: ParkingLotCreate,
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    db_lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    if not db_lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    db_lot.name = lot.name
    db_lot.address = lot.address
    db.commit()
    db.refresh(db_lot)
    return db_lot

# Delete a parking lot (admin only)
@router.delete("/{lot_id}", description="Admin only")
def delete_parking_lot(
    lot_id: int,
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    db_lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    if not db_lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    db.delete(db_lot)
    db.commit()
    return {"message": "Parking lot deleted"}