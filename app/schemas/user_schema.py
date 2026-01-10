from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role: str


class Token(BaseModel):
    access_token:str
    token_type: str