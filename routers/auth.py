from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import models
from schemas.user_request import UserRequest
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from schemas.token_squema import Token

# Router for authentication
router = APIRouter(
    prefix="/auth", 
    tags=["auth"]
)

# Security settings for JWT
SECRET_KEY = "234654gf8768fgf679867jgfsad1231254345sdfgds67532231dfghj67ui4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CryptContext for hashing passwords
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer instance for token authentication
oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

# Function to authenticate username and password
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

# Function to create access token
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to get current user from token
async def get_current_user(token: Annotated[str, Depends(oauth_bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if user_id is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

# POST users
@router.post("/createuser", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequest):
    create_user_model = models.User(
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        email=user_request.email,
        hashed_password=bcrypt_context.hash(user_request.password),
        role=user_request.role,
        is_active=True
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"message": "User created successfully", "user": create_user_model}

# POST token
@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

# GET users
@router.get("/users", status_code=status.HTTP_200_OK)
async def read_users(db: db_dependency):
    return db.query(models.User).all()

# DELETE users by userid
@router.delete("/deleteuser/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, user_id: int):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is not None:
        db.delete(user_model)
        db.commit()
        return {"message": f"User with id {user_id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found for deletion")