
# IMPORTS
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
import models
from schemas.todo_request import TodoRequest

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

# GET all todos
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(models.Todos).all()

# GET todos by id
@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

# GET todos by priority
@router.get("/priority", status_code=status.HTTP_200_OK)
async def read_by_priority(db: db_dependency, todo_priority: int = Query(le=6, gt=0)):
    todos = db.query(models.Todos).filter(models.Todos.priority == todo_priority).all()
    if todos:
        return todos
    raise HTTPException(status_code=404, detail=f"Todo with priority {todo_priority} not found")

# POST todos
@router.post("/createtodo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = models.Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return {"message": f"Todo with id {todo_model.id} created successfully", "todo": todo_model}

# PUT todos
@router.put("/updatetodo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
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
@router.delete("/deletetodo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is not None:
        db.delete(todo_model)
        db.commit()
        return {"message": f"Todo with id {todo_id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found for deletion")

