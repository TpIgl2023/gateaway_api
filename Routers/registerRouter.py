from fastapi import APIRouter
from pydantic import BaseModel

from Handlers.registerAccountHandler import registerAccountHandler

registerRouter = APIRouter()

class registerRequest(BaseModel):
    name: str 
    email: str 
    password: str 
    phone: str 
    
@registerRouter.post("/")
async def registerAccount(register_data : registerRequest):
    name = register_data.name
    email = register_data.email
    password = register_data.password
    phone = register_data.phone
    return await registerAccountHandler(email, name, password, phone)