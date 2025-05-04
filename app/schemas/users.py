import enum
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# enums for the roles.
class UserRoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"
    attendant = "attendant"

class UserBase(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    phone: str
    vehicle_number: str
    role: UserRoleEnum = UserRoleEnum.user

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True