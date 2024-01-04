import jwt
from starlette import status
from starlette.responses import JSONResponse

from Core.Environment.env import HASHING_SECRET_KEY, HASH_ALGORITHM
from Core.Shared.DatabaseOperations import Database
import requests
import json

from Services.authServices import decodeJwtToken


async def deleteUserHandler(userToken):
    try:

        payload = jwt.decode(userToken, HASHING_SECRET_KEY, algorithms=[HASH_ALGORITHM])
        email: str = payload.get("email")

        if email == None:
            raise Exception("Invalid token")

        email = email.lower()

        userResponse = Database.getAccountsWithFilter({"email":email})
        deleteAccouts = []
        if (userResponse["message"] == "Accounts retrieved successfully"):
            users = userResponse["accounts"]
            if len(users) != 0:
                for user in users:
                    Database.deleteUser(str(user["id"]))
                    deleteAccouts.append(user["id"])
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "message": "User deleted successfully",
                    "deletedAccountsId": deleteAccouts
                })

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": "Invalid email or password"
            })



        response = {
            "message": user
        }

        return response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error while deleting user",
                "error": str(e)
            })