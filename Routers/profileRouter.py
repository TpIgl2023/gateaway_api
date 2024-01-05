from fastapi import APIRouter
from Handlers.profileHandler import deleteUserHandler
from fastapi import Depends, FastAPI, HTTPException, Request

from fastapi.security import OAuth2PasswordBearer



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


profileRouter = APIRouter()

@profileRouter.delete("/")
async def deleteUserRoute(user : str = Depends(oauth2_scheme)):
    return await deleteUserHandler(user)