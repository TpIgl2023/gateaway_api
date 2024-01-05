from starlette import status
from starlette.responses import JSONResponse
from Core.Environment.databaseServiceEnv import DATABASE_SERVICE_API_KEY, DATABASE_API_URL
from Core.Shared.DatabaseOperations import Database
import requests
import json

from Services.authServices import validations, createJwtToken, errorsTypes


async def modifyPersonalInfoHandler(name, email, phone):
    try:
        hasError = False
        errorMessage = []
        if (validations.validate_name(name) == False):
            hasError = True
            errorMessage.append(errorsTypes.nameInvalid)
        if (validations.validate_email_syntax(email) == False):
            hasError = True
            errorMessage.append(errorsTypes.emailInvalid)
        if (validations.validate_mobile(phone) == False):
            hasError = True
            errorMessage.append(errorsTypes.mobileInvalid)
        
        if hasError:
            return JSONResponse(status_code=400,
                                content={
                                    "success" : "false",
                                    "message": f'Editing information failed with errors {errorMessage}'})
        
        usersResponse = Database.getAccountsWithFilter({"email":email})
        users = usersResponse["accounts"]
        updated_user = users[0]
        response = Database.updateUser(updated_user)
        
        return response
        """
        return JSONResponse(
            status_code=200,
            content={
                "success":True,
                "message":"Password updated successfully"
            }
        )
        
        """
        


    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "message": "Error while updating moderator",
                "error": str(e)
            })


