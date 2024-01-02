from datetime import datetime, timedelta
from Core.Environment.env import HASH_ALGORITHM , HASHING_SECRET_KEY , TOKEN_LIFE_TIME,HASHING_SALT
from typing import Optional
from base64 import b64decode
from fastapi import  HTTPException ,status
import jwt
from jwt import PyJWTError
import re
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
import hashlib



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

def createJwtToken(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_LIFE_TIME)  # Default expiration time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, HASHING_SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt




class errorsTypes:
    emailInvalid = "Invalid email"
    mobileInvalid = "Invalid mobile"
    nameInvalid = "Invalid name"


class validations:

    def validate_email_syntax(email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    def validate_password(passwd):
        SpecialSym = ['$', '@', '#', '%']
        val = True
        missings = []
        if len(passwd) < 6:
            missings.append('length should be at least 6')
            val = False
        if not any(char.isdigit() for char in passwd):
            missings.append('Password should have at least one numeral')
            val = False
        if not any(char.isupper() for char in passwd):
            missings.append('Password should have at least one uppercase letter')
            val = False
        if not any(char.islower() for char in passwd):
            missings.append('Password should have at least one lowercase letter')
            val = False
        if not any(char in SpecialSym for char in passwd):
            missings.append('Password should have at least one of the symbols $@#%')
            val = False
        return val, missings

    def validate_mobile(mobile):
        return carrier._is_mobile(number_type(phonenumbers.parse(mobile)))
        # return True

    def validate_name(name):
        if (name.replace(" ", "").isalpha()):
            return True
        else:
            return False


def hashString(string):
    salt = HASHING_SALT.encode('utf-8')
    # Combine password and salt, then hash
    string_salt_combo = string.encode('utf-8') + salt
    hashed_string = hashlib.sha256(string_salt_combo).hexdigest()
    print(hashed_string)
    return hashed_string



def validate_email_syntax(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True


def validate_mobile(mobile):
    return carrier._is_mobile(number_type(phonenumbers.parse(mobile)))

def validate_name(name):
    if (name.replace(" ", "").isalpha() & len(name) < 20):
        return True
    else:
        return False



from fastapi.security import OAuth2PasswordBearer

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
        print(payload)
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