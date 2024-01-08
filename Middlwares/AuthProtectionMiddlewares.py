from fastapi import Depends, FastAPI, HTTPException, Request

from fastapi.security import OAuth2PasswordBearer

from Core.UserStatus import UserStatus
from Core.statusProtected import statusProtected, privilege_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def isAdminProtected(token: str = Depends(oauth2_scheme)):
    print("token is : " + token)
    return statusProtected(token , UserStatus.ADMINISTRATOR)

def isModeratorProtected(token: str = Depends(oauth2_scheme)):
    return statusProtected(token , UserStatus.MODERATOR)

def isUserProtected(token: str = Depends(oauth2_scheme)):
    return statusProtected(token , UserStatus.USER)


def isUserAndModProtected(token: str = Depends(oauth2_scheme)):
    for status in [UserStatus.USER, UserStatus.MODERATOR]:
        try:
            return statusProtected(token, status)
        except privilege_exception:
            continue
    raise privilege_exception

