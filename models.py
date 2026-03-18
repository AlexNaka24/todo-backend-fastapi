# IMPORTS
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

# This is the model of the users table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String, nullable=True)


# This is the model of the todos table, it has a foreign key to the users table
class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String)
    priority = Column(Integer, index=True)
    complete = Column(Boolean, index=True, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))