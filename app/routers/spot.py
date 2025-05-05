from fastapi import APIRouter, HTTPException, Depends
from typing import List, Annotated
from sqlalchemy.orm import Session
from app.models.parkinglot import Spot
from app.schemas.parkinglot import SpotCreate, SpotOut
from app.database import SessionLocal
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/spot",
    tags=["spot"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/", response_model=SpotOut)
def create_spot(spot: SpotCreate, db: db_dependency, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    db_spot = Spot(floor_id=spot.floor_id, spot_number=spot.spot_number)
    db.add(db_spot)
    db.commit()
    db.refresh(db_spot)
    return db_spot

@router.get("/", response_model=List[SpotOut])
def get_spots(db: db_dependency, user: user_dependency):
    return db.query(Spot).all()

@router.get("/{spot_id}", response_model=SpotOut)
def get_spot(spot_id: int, db: db_dependency, user: user_dependency):
    spot = db.query(Spot).filter(Spot.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    return spot

@router.put("/{spot_id}", response_model=SpotOut)
def update_spot(spot_id: int, spot: SpotCreate, db: db_dependency, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    db_spot = db.query(Spot).filter(Spot.id == spot_id).first()
    if not db_spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    db_spot.floor_id = spot.floor_id
    db_spot.spot_number = spot.spot_number
    db.commit()
    db.refresh(db_spot)
    return db_spot

@router.delete("/{spot_id}")
def delete_spot(spot_id: int, db: db_dependency, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    db_spot = db.query(Spot).filter(Spot.id == spot_id).first()
    if not db_spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    db.delete(db_spot)
    db.commit()
    return {"message": "Spot deleted"}