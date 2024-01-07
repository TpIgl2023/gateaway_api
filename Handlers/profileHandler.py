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
        id: str = payload.get("id")

        if id == None:
            raise Exception("Invalid token")


        dbResponse = Database.deleteUser(id)
        if (dbResponse["message"] != "Account deleted successfully"):
            raise Exception(dbResponse["message"])


        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "User deleted successfully",
                "deletedAccountsId": id
            })

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": "Invalid email or password"
            })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error while deleting user",
                "error": str(e)
            })