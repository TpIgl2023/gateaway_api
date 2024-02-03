from fastapi import Depends, FastAPI, HTTPException, Request

from fastapi.security import OAuth2PasswordBearer

from Core.UserStatus import UserStatus
from Core.statusProtected import statusProtected, privilege_exception, statusProtectedForMulti

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
            # Attempt to get user ID for each status
            user_id = statusProtectedForMulti(token, status)
            if not user_id: continue
            # If successful, return the user ID
            return user_id
        except HTTPException as e:
            # Propagate HTTPException
            raise e
        except Exception:
            # Log unexpected errors for debugging
            pass

    # If none of the statuses match, raise privilege_exception
    raise privilege_exception



