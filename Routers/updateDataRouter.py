from fastapi import APIRouter
from Handlers.profileHandler import deleteUserHandler
from Handlers.modifyPasswordHandler import modifyPasswordHandler
from Handlers.modifyPersonalInfoHandler import modifyPersonalInfoHandler
from fastapi import Depends, FastAPI, HTTPException, Request

from fastapi.security import OAuth2PasswordBearer

from Models.updateInfoModel import modifyPasswordRequest, updateProfileRequest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


updateDataRouter = APIRouter()



@updateDataRouter.put("/updateprofile")
async def updateprofile(data : updateProfileRequest):
    name = data.name
    email = data.email
    phone = data.phone
    return await modifyPersonalInfoHandler(name, email, phone)



@updateDataRouter.put("/updatepassword")
async def updatePasswordRoute(data : modifyPasswordRequest):
    email = data.email
    oldPassword = data.oldpassword
    newPassword = data.newpassword
    return await modifyPasswordHandler(email, oldPassword, newPassword)