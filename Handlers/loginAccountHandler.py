import json

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from typing import Optional
from starlette.responses import JSONResponse

from Core.create_jwt_token import create_jwt_token
from Core.decode_jwt_token import decode_jwt_token
from Core.getAccountsWithFilter import getAccountsWithFilter
from Core.hashString import hashString

app = FastAPI()



# Example user data (in a real application, you'd have a user database)
fake_users_db = {
    "fakeuser": {
        "username": "fakeuser",
        "hashed_password": "fakehashedpassword"
    }
}

# OAuth2PasswordBearer for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def loginAccountHandler(email, password):
    try:
        password = hashString(password)

        usersResponse = getAccountsWithFilter({"email":email})
        # Check if the user exists
        if (usersResponse["message"] == "Accounts retrieved successfully"):
            users = usersResponse["accounts"]
            if len(users) != 0:
                for user in users:
                    if user["password"] == password:
                        token_data = {"sub": user["email"]}
                        jwt_token = create_jwt_token(token_data)
                        response = JSONResponse(content={"success":True})
                        response.headers["Authorization"] = f"Bearer {jwt_token}"
                        response.set_cookie(key="access_token", value=jwt_token,httponly=True)
                        return response
        response = JSONResponse(content={"success": False,"message":"Invalid email or password"})
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error while sending request to database-service",
                "error": str(e)
            })