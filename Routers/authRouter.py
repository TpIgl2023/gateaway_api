from Handlers.authHandlers import loginAccountHandler
from fastapi import APIRouter, Depends

from Models.RequestsModels import LoginRequest , registerRequest

from Handlers.authHandlers import registerUserAccountHandler

authRouter = APIRouter()

@authRouter.post("/login")
async def loginAccount(login_data: LoginRequest):

    email = login_data.email
    password = login_data.password
    return await loginAccountHandler(email, password)


@authRouter.post("/register/user")
async def registerUserAccount(register_data: registerRequest ):
    name = register_data.name
    email = register_data.email
    password = register_data.password
    phone = register_data.phone
    return await registerUserAccountHandler(name, email, password, phone)

