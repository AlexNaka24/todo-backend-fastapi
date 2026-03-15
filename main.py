
# IMPORTS
from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos

# Create FastAPI instance
app = FastAPI()

# Creates all tables of the database defined in models if they dont exist
models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)
