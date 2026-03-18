from pydantic import BaseModel, Field

# This is the schema for the request body of the POST endpoint of the user verification router
class UserVerification(BaseModel):
    current_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)