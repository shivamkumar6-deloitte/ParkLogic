from fastapi import APIRouter, HTTPException, Depends
from typing import List, Annotated
from sqlalchemy.orm import Session
from app.models.parkinglot import Floor
from app.schemas.parkinglot import FloorCreate, FloorOut
from app.database import SessionLocal
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/floor",
    tags=["floor"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/", response_model=FloorOut)
def create_floor(floor: FloorCreate, db: db_dependency, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    db_floor = Floor(parking_lot_id=floor.parking_lot_id, floor_number=floor.floor_number)
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)
    return db_floor

@router.get("/", response_model=List[FloorOut])
def get_floors(db: db_dependency, user: user_dependency):
    return db.query(Floor).all()

@router.get("/{floor_id}", response_model=FloorOut)
def get_floor(floor_id: int, db: db_dependency, user: user_dependency):
    floor = db.query(Floor).filter(Floor.id == floor_id).first()
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    return floor

@router.put("/{floor_id}", response_model=FloorOut)
def update_floor(floor_id: int, floor: FloorCreate, db: db_dependency, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    db_floor = db.query(Floor).filter(Floor.id == floor_id).first()
    if not db_floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    db_floor.parking_lot_id = floor.parking_lot_id
    db_floor.floor_number = floor.floor_number
    db.commit()
    db.refresh(db_floor)
    return db_floor

@router.delete("/{floor_id}")
def delete_floor(floor_id: int, db: db_dependency, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    db_floor = db.query(Floor).filter(Floor.id == floor_id).first()
    if not db_floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    db.delete(db_floor)
    db.commit()
    return {"message": "Floor deleted"}