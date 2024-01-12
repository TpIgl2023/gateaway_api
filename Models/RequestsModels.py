from pydantic import BaseModel

class ExtractionRequest(BaseModel):
    URL: str

class registerRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ModifyPasswordRequest(BaseModel):
    oldPassword: str
    newPassword: str