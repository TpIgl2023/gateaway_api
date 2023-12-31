from fastapi import Depends

from fastapi.security import OAuth2PasswordBearer

from Core.Shared.UserStatus import UserStatus
from Services.authServices import statusProtected

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def isAdminProtected(token: str = Depends(oauth2_scheme)):
    print("token is : " + token)
    return statusProtected(token , UserStatus.ADMINISTRATOR)