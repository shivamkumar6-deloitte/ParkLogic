import os
import enum
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta, datetime, timezone
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from ..models.users import Users
from ..database import SessionLocal

router= APIRouter(
    prefix='/auth',
    tags=['/auth']
)

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

#pydantics class for request validation

class UserRoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"
    attendant = "attendant"

class CreateUserRequest(BaseModel):
    name : str = Field(min_length=2)
    email : str = Field(min_length=5) #x@x.xx 6 chars
    phone : str
    vehicle_number: str
    password: str = Field(min_length=8)
    role: UserRoleEnum = UserRoleEnum.user

class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user (email: str, password: str, db):
    user =db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(email: str, user_id: int, role: str, expires_delta: timedelta):
    encode_payload = {'sub': email, 'id': user_id, 'role': role}

    expires = datetime.now(timezone.utc) + expires_delta
    encode_payload.update({'exp': expires})
    return jwt.encode(encode_payload,key=SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        email: str = payload.get('sub')
        user_id: str = payload.get('id')
        role: str = payload.get('role')
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validate creds')
        return {'email': email, 'user_id': user_id, 'role': role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validate creds')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_req: CreateUserRequest):
    create_user_model = Users(
        email = create_user_req.email,
        name = create_user_req.name,
        phone = create_user_req.phone,
        vehicle_number = create_user_req.vehicle_number,
        role = create_user_req.role,
        hashed_password= bcrypt_context.hash(create_user_req.password)
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"message": "User created successfully", "user_id": create_user_model.id}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                      detail='could not validate creds')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}

