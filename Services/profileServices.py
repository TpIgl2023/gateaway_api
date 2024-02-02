from starlette import status
from starlette.responses import JSONResponse
from Core.Environment.pdfServiceEnv import PDF_SERVICE_API_KEY, PDF_SERVICE_API_URL
from Core.Environment.databaseServiceEnv import DATABASE_SERVICE_API_KEY, DATABASE_API_URL
from Services.authServices import validations, createJwtToken, errorsTypes, hashString, errorsTypes
from Services.adminServices import is_url, is_int, isModerator
from Core.Shared.DatabaseOperations import Database
import requests
import json
import jwt
from Core.Environment.env import HASHING_SECRET_KEY, HASH_ALGORITHM



async def modifyUserPassword(id, oldPassword, newPassword):
        if (oldPassword == newPassword):
            raise Exception("The old and new password must be different")

        # Check if the password is valid
        (val, missings) = validations.validate_password(newPassword)
        if not val:
            return JSONResponse(
                content={"success": False,
                         "message":missings})

        response = await Database.getAccountWithId(id)
        if (response["message"] == "Account retrieved successfully"):
            user= response["account"]

            if user["password"] == hashString(oldPassword):
                user["password"] = hashString(newPassword)
                response = await Database.updateUser(user)
                if response["message"] == "Account updated successfully":
                    return {"success":True , "message":"Password updated successfully"}
                else:
                    raise Exception("Error while updating user password , database-service error")
            else:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "success": False,
                        "message":"Old password is incorrect"
                    })
        else:
            raise Exception("User not found")


async def modifyPersonalInfo(updated_user):
        if "id" not in updated_user:
            return JSONResponse(status_code=400,
                                content={
                                    "success":"false",
                                    "message": "Missing id"})

        hasError = False
        errorMessage = []


        if "email" in updated_user:
            email = updated_user["email"]
            updated_user["email"] = email.lower()
            if not validations.validate_email_syntax(updated_user["email"]):
                hasError = True
                errorMessage.append(errorsTypes.emailInvalid)

        if "password" in updated_user:
            del updated_user["password"]

        if "phone" in updated_user:
            if not validations.validate_mobile(updated_user["phone"]):
                hasError = True
                errorMessage.append(errorsTypes.mobileInvalid)

        if "name" in updated_user:
            if not validations.validate_name(updated_user["name"]):
                hasError = True
                errorMessage.append(errorsTypes.nameInvalid)

        if hasError:
            return JSONResponse(status_code=400,
                                content={
                                    "success": "false",
                                    "message": errorMessage
                                })



        response = await Database.updateUser(updated_user)
        if response["message"] == "Account updated successfully":
            return {"success":True , "message":"Account updated successfully"}
        else:
            raise Exception("Error while updating user , database-service error")