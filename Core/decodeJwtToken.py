from base64 import b64decode

from fastapi import  HTTPException ,status
import jwt
from jwt import PyJWTError
from Core.Environment.env import HASHING_SECRET_KEY, HASH_ALGORITHM



def decodeJwtToken(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, b64decode(HASHING_SECRET_KEY), algorithms=[HASH_ALGORITHM])
        print(payload)
        return payload
    except PyJWTError:
        raise credentials_exception