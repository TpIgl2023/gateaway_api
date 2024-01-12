from fastapi import APIRouter
from Handlers.profileHandler import deleteUserHandler, getProfileHandler, modifyPersonalInfoHandler, \
    modifyPasswordHandler
from fastapi import Depends, FastAPI, HTTPException, Request
from Models.RequestsModels import ModifyPasswordRequest

from fastapi.security import OAuth2PasswordBearer



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


profileRouter = APIRouter()

@profileRouter.delete("/")
async def deleteUserRoute(user : str = Depends(oauth2_scheme)):
    return await deleteUserHandler(user)


@profileRouter.get("/")
async def getProfileRoute(user : str = Depends(oauth2_scheme)):
    return await getProfileHandler(user)

@profileRouter.put("/")
async def updateProfileRoute(updated_user : dict ,user : str = Depends(oauth2_scheme)):
    return await modifyPersonalInfoHandler(user,updated_user)

@profileRouter.put("/password")
async def updatePasswordRoute(request : ModifyPasswordRequest  ,user : str = Depends(oauth2_scheme)):
    oldPassword = request.oldPassword
    newPassword = request.newPassword
    return await modifyPasswordHandler(user,oldPassword,newPassword)