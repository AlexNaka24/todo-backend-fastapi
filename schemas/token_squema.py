from pydantic import BaseModel

# This is the schema for the response body of the POST endpoint of the auth router, it contains the access token and the token type
class Token(BaseModel):
    access_token: str
    token_type: str