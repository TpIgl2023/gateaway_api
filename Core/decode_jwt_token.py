from fastapi import  HTTPException ,status
import jwt
from jwt import PyJWTError
from env import HASHING_SECRET_KEY, HASH_ALGORITHM



def decode_jwt_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, HASHING_SECRET_KEY, algorithms=[HASH_ALGORITHM])
        return payload
    except PyJWTError:
        raise credentials_exception