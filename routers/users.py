from fastapi import APIRouter, Body, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
import models
from routers.auth import get_current_user
from passlib.context import CryptContext
from schemas.user_verification import UserVerification

# Router for users
router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# Creates a new session for each petition and then it closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CryptContext for hashing passwords
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer instance for token authentication
oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# Dependency for database session
db_dependency = Annotated[Session, Depends(get_db)]

# Dependency for current user from token
user_dependency = Annotated[dict, Depends(get_current_user)]

# GET current user logged in
@router.get("/me", status_code=status.HTTP_200_OK)
async def read_current_user(current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource")
    return current_user

# CHANGE password of current user logged in
@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(db: db_dependency, current_user: user_dependency, user_verification: UserVerification):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource")
    user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Verify current password
    if not bcrypt_context.verify(user_verification.current_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    user.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.commit()
    return {"message": "Password changed successfully"}

@router.put("/change-phone", status_code=status.HTTP_200_OK)
async def change_phone_number(db: db_dependency, current_user: user_dependency, phone_number: str = Body(min_length=10, max_length=20, embed=True)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource")
    user = db.query(models.User).filter(models.User.id == current_user["id"]).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.phone_number = phone_number
    db.commit()
    return {"message": "Phone number changed successfully"}