from fastapi import APIRouter
from Handlers.modifyPasswordHandler import modifyPasswordHandler
from Handlers.modifyPersonalInfoHandler import modifyPersonalInfoHandler

from fastapi.security import OAuth2PasswordBearer

from Models.updateInfoModel import modifyPasswordRequest, updateProfileRequest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


updateDataRouter = APIRouter()



@updateDataRouter.put("/updateprofile")
async def updateprofile(data : updateProfileRequest):
    token = data.token
    name = data.name
    email = data.email
    phone = data.phone
    return await modifyPersonalInfoHandler(token, name, email, phone)



@updateDataRouter.put("/updatepassword")
async def updatePasswordRoute(data : modifyPasswordRequest):
    token = data.token
    email = data.email
    oldPassword = data.oldpassword
    newPassword = data.newpassword
    return await modifyPasswordHandler(token, email, oldPassword, newPassword)