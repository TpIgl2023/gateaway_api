from base64 import b64decode
from datetime import datetime, timedelta
import jwt
from env import HASH_ALGORITHM , HASHING_SECRET_KEY , TOKEN_LIFE_TIME
from typing import Optional


def createJwtToken(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_LIFE_TIME)  # Default expiration time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, HASHING_SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt



