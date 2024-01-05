from pydantic import BaseModel

class modifyPasswordRequest(BaseModel):
    email: str
    oldpassword: str
    newpassword: str

class updateProfileRequest(BaseModel):
    name: str
    email: str
    phone: str
    

