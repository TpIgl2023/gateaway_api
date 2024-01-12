import jwt
from starlette import status
from starlette.responses import JSONResponse

from Core.Environment.env import HASHING_SECRET_KEY, HASH_ALGORITHM
from Core.Shared.DatabaseOperations import Database
import requests
import json

from Services.authServices import decodeJwtToken
from Services.profileServices import modifyUserPassword, modifyPersonalInfo


async def deleteUserHandler(userToken):
    try:

        payload = jwt.decode(userToken, HASHING_SECRET_KEY, algorithms=[HASH_ALGORITHM])
        id: str = payload.get("id")

        if id == None:
            raise Exception("Invalid token")


        dbResponse = await Database.deleteUser(id)
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


async def getProfileHandler(userToken):
    try:

        payload = jwt.decode(userToken, HASHING_SECRET_KEY, algorithms=[HASH_ALGORITHM])
        id: str = payload.get("id")

        if id == None:
            raise Exception("Invalid token")


        dbResponse = await Database.getAccountWithId(id)
        if (dbResponse["message"] != "Account retrieved successfully"):
            raise Exception(dbResponse["message"])

        user = dbResponse["account"]
        del user["password"]
        del user["id"]


        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "user": user
            })



    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error while getting user info",
                "error": str(e)
            })


async def modifyPasswordHandler(userToken, oldPassword, newPassword):
    try:
        payload = jwt.decode(userToken, HASHING_SECRET_KEY, algorithms=[HASH_ALGORITHM])
        id: str = payload.get("id")

        if id == None:
            raise Exception("Invalid token")

        id = int(id)

        return await modifyUserPassword(id, oldPassword, newPassword)

    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "success": False,
                "message": "Error while modifying password",
                "error": str(e)
            })

async def modifyPersonalInfoHandler(userToken, updated_user):
    try:
        payload = jwt.decode(userToken, HASHING_SECRET_KEY, algorithms=[HASH_ALGORITHM])
        id: str = payload.get("id")

        if id == None:
            raise Exception("Invalid token")

        id = int(id)

        updated_user["id"] = id

        return await modifyPersonalInfo(updated_user)

    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "success": False,
                "message": "Error while modifying personal info",
                "error": str(e)
            })