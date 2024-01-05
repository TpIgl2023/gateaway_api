from pydantic import BaseModel

class modifyPasswordRequest(BaseModel):
    token: str
    email: str
    oldpassword: str
    newpassword: str

class updateProfileRequest(BaseModel):
    token: str
    name: str
    email: str
    phone: str
    

