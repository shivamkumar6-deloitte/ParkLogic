from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Annotated
from sqlalchemy.orm import Session
from app.models.parkingRecords import ParkingRecords, ParkingPurposeEnum
from app.models.parkinglot import Spot
from app.schemas.parkingRecords import ParkingRecordCreate, ParkingRecordOut
from app.database import SessionLocal
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/booking",
    tags=["booking"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Book a spot (user only)
@router.post("/", response_model=ParkingRecordOut, description="Users only: Book a parking spot.")
def book_spot(
    booking: ParkingRecordCreate,
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') != 'user':
        raise HTTPException(status_code=403, detail="Users only can book spots.")

    # Check if spot is already booked or under maintenance (active record with no exit_time)
    active_record = db.query(ParkingRecords).filter(
        ParkingRecords.spot_id == booking.spot_id,
        ParkingRecords.exit_time == None
    ).first()
    if active_record:
        raise HTTPException(status_code=400, detail="Spot is already booked or under maintenance.")

    db_booking = ParkingRecords(
        user_id=user['user_id'],
        spot_id=booking.spot_id,
        purpose=ParkingPurposeEnum.booking
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

#View own bookings (user)
@router.get("/my", response_model=List[ParkingRecordOut], description="Users only: View your bookings.")
def get_my_bookings(
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') != 'user':
        raise HTTPException(status_code=403, detail="Users only.")
    bookings = db.query(ParkingRecords).filter(ParkingRecords.user_id == user['user_id']).all()
    return bookings

 #Cancel own booking (user)
@router.delete("/cancel/{booking_id}", description="Users only: Cancel your booking.")
def cancel_booking(
    booking_id: int,
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') != 'user':
        raise HTTPException(status_code=403, detail="Users only.")
    booking = db.query(ParkingRecords).filter(
        ParkingRecords.id == booking_id,
        ParkingRecords.user_id == user['user_id'],
        ParkingRecords.exit_time == None
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Active booking not found.")
    booking.exit_time = db.func.now()
    db.commit()
    return {"message": "Booking cancelled."}

#  Block/unblock spot for maintenance (admin/attendant)
@router.post("/maintenance/block", response_model=ParkingRecordOut, description="Admin/Attendant: Block a spot for maintenance.")
def block_spot_for_maintenance(
    booking: ParkingRecordCreate,
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') not in ['admin', 'attendant']:
        raise HTTPException(status_code=403, detail="Admins or attendants only.")

    # Check if spot is already booked or under maintenance
    active_record = db.query(ParkingRecords).filter(
        ParkingRecords.spot_id == booking.spot_id,
        ParkingRecords.exit_time == None
    ).first()
    if active_record:
        raise HTTPException(status_code=400, detail="Spot is already booked or under maintenance.")

    db_maintenance = ParkingRecords(
        user_id=user['user_id'],
        spot_id=booking.spot_id,
        purpose=ParkingPurposeEnum.maintenance
    )
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance

@router.post("/maintenance/unblock/{spot_id}", description="Admin/Attendant: Unblock a spot from maintenance.")
def unblock_spot_for_maintenance(
    spot_id: int,
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') not in ['admin', 'attendant']:
        raise HTTPException(status_code=403, detail="Admins or attendants only.")

    # Find active maintenance record for this spot
    maintenance_record = db.query(ParkingRecords).filter(
        ParkingRecords.spot_id == spot_id,
        ParkingRecords.purpose == ParkingPurposeEnum.maintenance,
        ParkingRecords.exit_time == None
    ).first()
    if not maintenance_record:
        raise HTTPException(status_code=404, detail="No active maintenance block found for this spot.")

    maintenance_record.exit_time = db.func.now()
    db.commit()
    return {"message": "Spot unblocked from maintenance."}

# View all bookings (admin/attendant)
@router.get("/all", response_model=List[ParkingRecordOut], description="Admin/Attendant: View all bookings.")
def get_all_bookings(
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get('role') not in ['admin', 'attendant']:
        raise HTTPException(status_code=403, detail="Admins or attendants only.")
    bookings = db.query(ParkingRecords).all()
    return bookings