from fastapi import APIRouter
from pydantic import BaseModel

from Handlers.loginAccountHandler import loginAccountHandler

loginRouter = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str



@loginRouter.post("/")
async def loginAccount(login_data: LoginRequest):
    email = login_data.email
    password = login_data.password
    return await loginAccountHandler(email, password)

