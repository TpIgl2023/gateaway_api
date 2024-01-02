from pydantic import BaseModel

class registerRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str

class LoginRequest(BaseModel):
    email: str
    password: str
