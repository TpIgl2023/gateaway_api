from starlette import status
from starlette.responses import JSONResponse
from Core.Environment.pdfServiceEnv import PDF_SERVICE_API_KEY, PDF_SERVICE_API_URL
from Core.Environment.databaseServiceEnv import DATABASE_SERVICE_API_KEY, DATABASE_API_URL
from Services.adminServices import is_url, is_int, isModerator
from Core.Shared.DatabaseOperations import Database
import requests
import json


from Services.authServices import validations, createJwtToken, hashString, errorsTypes

import jwt
from Core.Environment.env import HASHING_SECRET_KEY, HASH_ALGORITHM


async def modifyPasswordHandler(userToken, email, oldPassword, newPassword):
    try:
        """
        payload = jwt.decode(userToken, HASHING_SECRET_KEY, algorithms=[HASH_ALGORITHM])
        emailTest: str = payload.get("email")

        if emailTest == None:
            raise Exception("Invalid token")        
        """
        if (oldPassword == newPassword):
            raise Exception("The old and new password must be different")
        
        usersResponse = Database.getAccountsWithFilter({"email":email})
        if (usersResponse["message"] == "Accounts retrieved successfully"):
            users = usersResponse["accounts"]
            oldPasswordHash = hashString(oldPassword)
            if len(users) != 0:
                for user in users:
                    if user["password"] == oldPasswordHash:
                        errorMessage = []
                        hasError = False
                        (val,missings) =  validations.validate_password(newPassword)
                        if not val:
                            hasError = True
                            errorMessage.append(missings)
                        if (hasError):
                            return JSONResponse(
                                content={"success" : False,
                                        "message" : f'new password is invalid with errors {errorMessage}'}
                            )
                        
                        newPasswordHash = hashString(newPassword)
                        updated_user = users[0]
                        updated_user["password"] = newPasswordHash
                        response = Database.updateUser(updated_user)
                        return response
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message":"Old password is incorrect"
            })

    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "message": "Error while modifying password",
                "error": str(e)
            })


