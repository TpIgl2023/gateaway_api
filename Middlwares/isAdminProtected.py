from fastapi import Depends, FastAPI, HTTPException, Request

from fastapi.security import OAuth2PasswordBearer

from Core.UserStatus import UserStatus
from Core.statusProtected import statusProtected

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def isAdminProtected(token: str = Depends(oauth2_scheme)):
    print("token is : " + token)
    return statusProtected(token , UserStatus.ADMINISTRATOR)