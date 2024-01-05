from starlette.responses import JSONResponse
from Core.Shared.DatabaseOperations import Database


from Services.authServices import validations, createJwtToken, errorsTypes



async def modifyPersonalInfoHandler(userToken, name, email, phone):
    try:
        """
        payload = jwt.decode(userToken, HASHING_SECRET_KEY, algorithms=[HASH_ALGORITHM])
        emailTest: str = payload.get("email")

        if emailTest == None:
            raise Exception("Invalid token")
        """
        
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
        if (len(users) > 0):
            updated_user = users[0]
            updated_user["name"] = name
            updated_user["email"] = email
            updated_user["phone"] = phone
            response = Database.updateUser(updated_user)
            return response
        
        return JSONResponse(status_code=400,
                            content={
                                "success" : "false",
                                "message": f'Error when updating the user data : no users found with {email}'
                            })
        
    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "message": "Error while updating user",
                "error": str(e)
            })


