# IMPORTS
from fastapi import FastAPI
import models
from database import engine
from routers import admin, auth, todos, users

# Create FastAPI instance
app = FastAPI()

# Creates all tables of the database defined in models if they dont exist
models.Base.metadata.create_all(bind=engine)

# Health check endpoint
@app.get("/healthy")
def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)