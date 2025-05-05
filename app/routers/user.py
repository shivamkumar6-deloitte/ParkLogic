from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
from app.models.users import Users
from app.schemas.users import UserOut, UserCreate
from app.database import SessionLocal
from app.routers.auth import get_current_user, bcrypt_context
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

#   View own details
@router.get("/me", response_model=UserOut, description="Users only: View your profile.")
def get_my_profile(db: db_dependency, user: user_dependency):
    db_user = db.query(Users).filter(Users.id == user['user_id']).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#Update own details (except password and role)
@router.put("/me", response_model=UserOut, description="Users only: Update your profile (not password/role).")
def update_my_profile(
    update: UserCreate,
    db: db_dependency,
    user: user_dependency
):
    db_user = db.query(Users).filter(Users.id == user['user_id']).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = update.name
    db_user.email = update.email
    db_user.phone = update.phone
    db_user.vehicle_number = update.vehicle_number
    db.commit()
    db.refresh(db_user)
    return db_user

#  Change password, needs the old one as well befpre changing


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)

@router.put("/me/password", description="Users only: Change your password.")
def change_password(
    req: ChangePasswordRequest,
    db: db_dependency,
    user: user_dependency
):
    db_user = db.query(Users).filter(Users.id == user['user_id']).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt_context.verify(req.old_password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    db_user.hashed_password = bcrypt_context.hash(req.new_password)
    db.commit()
    return {"message": "Password changed successfully"}