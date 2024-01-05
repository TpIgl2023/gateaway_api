from starlette import status
from starlette.responses import JSONResponse
from Core.Environment.pdfServiceEnv import PDF_SERVICE_API_KEY, PDF_SERVICE_API_URL
from Core.Environment.databaseServiceEnv import DATABASE_SERVICE_API_KEY, DATABASE_API_URL
from Services.adminServices import is_url, is_int, isModerator
from Core.Shared.DatabaseOperations import Database
import requests
import json

from Services.authServices import validations, createJwtToken, hashString, errorsTypes

#! imports added now

async def modifyPasswordHandler(email, oldPassword, newPassword):
    try:
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
                        #! ********** Change the oldPassword to newPasswordHash in data set here *************
                        del user["password"]
                        userId = user["id"]
                        newPasswordHash = hashString(newPassword)
                        response = Database.updatePassword(userId, newPasswordHash)
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


