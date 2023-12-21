from fastapi import FastAPI, HTTPException
from fastapi import status
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from env import HASHING_SECRET_KEY , HASH_ALGORITHM

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
        detail={
            "success": False,
            "message": f"Could not validate credentials"},
    )

privilege_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    headers={"WWW-Authenticate": "Bearer"},
    detail = {
        "success":False,
        "message":"You don't have the privilege to access this resource"},
)

def statusProtected(token,status):
    try:
        payload = jwt.decode(token, HASHING_SECRET_KEY, algorithms=[HASH_ALGORITHM])
        email: str = payload.get("email")
        user_status : str = payload.get("status")
        if user_status != status:
            raise privilege_exception
        if email == None:
            raise credentials_exception

        # Else , continue. (Don't raise any exception)
        return email
    except HTTPException as e:
        raise e
    except Exception:
        raise credentials_exception


