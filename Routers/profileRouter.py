from fastapi import APIRouter
from Handlers.profileHandler import deleteUserHandler, getProfileHandler, modifyPersonalInfoHandler
from fastapi import Depends, FastAPI, HTTPException, Request

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