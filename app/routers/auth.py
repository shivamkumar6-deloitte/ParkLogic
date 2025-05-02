from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta, datetime, timezone
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from ..models.users import User
from ..database import SessionLocal

router= APIRouter(
    prefix='/auth'

)