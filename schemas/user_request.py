from pydantic import BaseModel, Field

# This is the schema for the request body of the POST and PUT endpoints of the users router
class UserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    first_name: str = Field(min_length=3, max_length=40)
    last_name: str = Field(min_length=3, max_length=40)
    email: str = Field(min_length=5, max_length=40)
    password: str = Field(min_length=6)
    role: str = Field(min_length=3, max_length=50)
    is_active: bool = Field(default=True)