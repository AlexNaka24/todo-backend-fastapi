# IMPORTS
from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionLocal
import models
from routers.auth import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session

# Router for admin
router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

# Creates a new session for each petition and then it closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for database session      
db_dependency = Annotated[Session, Depends(get_db)]

# Dependency for current user from token
user_dependency = Annotated[dict, Depends(get_current_user)]

# GET all todos (only for admin)
@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all_todos(db: db_dependency, user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource, you are not an admin")
    return db.query(models.Todos).all()

# GET all users
@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependency, user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource, you are not an admin")
    return db.query(models.User).all()

# GET user by id
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user_by_id(db: db_dependency, user: user_dependency, user_id: int):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource, you are not an admin")
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} was not found")
    return f"User with id {user_id} was found", f"User: {user_model.first_name} {user_model.last_name}, username: {user_model.username}, role: {user_model.role}"

# GET user by username
@router.get("/users/username/{username}", status_code=status.HTTP_200_OK)
async def read_user_by_username(db: db_dependency, user: user_dependency, username: str):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource, you are not an admin")
    user_model = db.query(models.User).filter(models.User.username == username).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} was not found")
    return f"User with username {username} was found", f"User: {user_model.first_name} {user_model.last_name}, username: {user_model.username}, role: {user_model.role}"

# DELETE user by id
@router.delete("/users/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_by_id(db: db_dependency, user: user_dependency, user_id: int):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource, you are not an admin")
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} was not found")
    todos = db.query(models.Todos).filter(models.Todos.owner_id == user_id).all()
    for todo in todos:
        db.delete(todo)
    db.delete(user_model)
    db.commit()
    db.refresh(user_model)
    return f"User with id {user_id} was deleted" 