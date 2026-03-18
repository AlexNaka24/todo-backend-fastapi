# IMPORTS
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
import models
from schemas.todo_request import TodoRequest
from routers.auth import get_current_user

# Router for todos
router = APIRouter(
    prefix="/todos", 
    tags=["todos"]
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

# GET all todos from your profile or all todos if you are an admin
@router.get("", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access todos")
    if user.get("role") == "admin":
        return db.query(models.Todos).all()
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()

# GET todos by id
@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this todo")
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id, models.Todos.owner_id == user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

# GET todos by priority
@router.get("/priority/{todo_priority}", status_code=status.HTTP_200_OK)
async def read_by_priority(db: db_dependency, user: user_dependency, todo_priority: int = Path(le=5, gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this todo")
    todos = db.query(models.Todos).filter(models.Todos.priority == todo_priority, models.Todos.owner_id == user.get("id")).all()
    if todos:
        return todos
    raise HTTPException(status_code=404, detail=f"Todo with priority {todo_priority} not found")

# POST todos
@router.post("/create-todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, user: user_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to create a todo")   
    todo_model = models.Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return {"message": f"Todo with id {todo_model.id} created successfully", "todo": todo_model}

# PUT todos
@router.put("/update-todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(db: db_dependency, user: user_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to update this todo")
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id, models.Todos.owner_id == user.get("id")).first()
    if todo_model is not None:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority 
        todo_model.complete = todo_request.complete
        db.commit()
        db.refresh(todo_model)
        return {"message": f"Todo with id {todo_id} updated successfully", "todo": todo_model}
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found for updates")

# DELETE todos
@router.delete("/delete-todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to delete this todo")
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id, models.Todos.owner_id == user.get("id")).first()
    if todo_model is not None:
        db.delete(todo_model)
        db.commit()
        return {"message": f"Todo with id {todo_id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found for deletion")

