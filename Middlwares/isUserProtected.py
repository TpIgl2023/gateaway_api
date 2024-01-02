from fastapi import Depends, FastAPI, HTTPException, Request

from fastapi.security import OAuth2PasswordBearer

from Core.UserStatus import UserStatus
from Core.statusProtected import statusProtected

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def isUserProtected(token: str = Depends(oauth2_scheme)):
    return statusProtected(token , UserStatus.USER)