from fastapi import Depends

from fastapi.security import OAuth2PasswordBearer

from Core.Shared.UserStatus import UserStatus
from Services.authServices import statusProtected

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def isUserProtected(token: str = Depends(oauth2_scheme)):
    return statusProtected(token , UserStatus.USER)