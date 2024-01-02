from Handlers.authHandlers import loginAccountHandler
from fastapi import APIRouter, Depends

from Middlwares.AuthProtectionMiddlewares import isAdminProtected
from Models.AuthModels import LoginRequest , registerRequest

from Handlers.authHandlers import registerUserAccountHandler , registerModeratorAccountHandler

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

@authRouter.post("/register/moderator")
async def registerModeratorAccount(register_data: registerRequest, user: str = Depends(isAdminProtected)):
    name = register_data.name
    email = register_data.email
    password = register_data.password
    phone = register_data.phone
    return await registerModeratorAccountHandler(name, email, password, phone)