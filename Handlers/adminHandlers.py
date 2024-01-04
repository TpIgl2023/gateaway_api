from starlette import status
from starlette.responses import JSONResponse
from Core.Environment.pdfServiceEnv import PDF_SERVICE_API_KEY, PDF_SERVICE_API_URL
from Core.Environment.databaseServiceEnv import DATABASE_SERVICE_API_KEY, DATABASE_API_URL
from Services.adminServices import is_url, is_int, isModerator
from Core.Shared.DatabaseOperations import Database
import requests
import json

from Services.authServices import validations, createJwtToken, hashString, errorsTypes


async def ExtractFromPdf(URL):
    try:
        if not is_url(URL):
            return JSONResponse(
                status_code=400,
                content={"message": "URL is not valid"})

        headers = {'x-api-key': PDF_SERVICE_API_KEY}

        params = {'URL': URL}

        response = requests.get(PDF_SERVICE_API_URL, headers=headers, params=params)

        return response.json()

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error while extracting data from PDF",
                "error": str(e)
            })


async def getAllModerators():
    try:
        response = Database.getAllModerators()
        return response.json()
    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "message": "Error while getting moderators",
                "error": str(e)
            })


async def adminRestrictedPageHandler():
    try:
        return {"Hello": "Admin !"}
    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "message": "Error while sending request to database-service",
                "error": str(e)
            })


async def deleteModerator(id):
    try:
        isMod = isModerator(id)

        if type(isMod) != bool:
            return isMod

        if not isMod:
            return JSONResponse(status_code=400,
                content={
                    "message": "User is not a moderator"
                })

        # Delete the user
        response = Database.deleteUser(str(id))
        return response
    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "message": "Error while deleting moderator",
                "error": str(e)
            })

async def registerModeratorAccountHandler(name, email, password, phone):
    try:
        lowerCaseEmail = email.lower()
        # check if the fields are valid
        emailIsValid = validations.validate_email_syntax(lowerCaseEmail)
        passwordIsValid, _ = validations.validate_password(password)
        mobileIsValid = validations.validate_mobile(phone)
        nameIsValid = validations.validate_name(name)
        errors = []
        if (emailIsValid & passwordIsValid & mobileIsValid & nameIsValid):
            usersResponse = Database.getAccountsWithFilter({"email": lowerCaseEmail})
            # check if email exists
            users = usersResponse["accounts"]
            if (len(users) == 0):
                # generating the token
                token_data = {"email": lowerCaseEmail, "status": "moderator"}
                jwt_token = createJwtToken(token_data)
                password = hashString(password)
                user = {
                    "name": name,
                    "email": lowerCaseEmail,
                    "password": password,
                    "phone": phone
                }
                Database.createUser(user, "moderator")
                del user["password"]
                response = JSONResponse(
                    content={"success": True, "message": "User created succesfully", "user": user},
                    headers={"Authorization": f"Bearer {jwt_token}"},
                )
                response.set_cookie(key="Authorization", value=jwt_token, httponly=True)
                return response
            else:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "success": False,
                        "message": "This Email is already used"
                    })
        else:
            passwordValid, passwordErrors = validations.validate_password(password)
            if (not validations.validate_email_syntax(email)):
                errors.append(errorsTypes.emailInvalid)
            if (not validations.validate_name(name)):
                errors.append(errorsTypes.nameInvalid)
            if (not passwordValid):
                errors.append(passwordErrors)
            if (not validations.validate_mobile(phone)):
                errors.append(errorsTypes.mobileInvalid)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "message": errors
                })

    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={
                "message": "error while registering user. got an Exception",
                "error": str(e)
            }
        )


async def editModeratorAccountHandler(updated_user):
    try:

        if "id" not in updated_user:
            return JSONResponse(status_code=400,
                                content={
                                    "message": "Missing moderator id"})

        id = updated_user["id"]

        isMod = isModerator(id)

        if type(isMod) != bool:
            return isMod

        if not isMod:
            return JSONResponse(status_code=400,
                                content={
                                    "success":"false",
                                    "message": "User is not a moderator"
                                })
        if (not is_int(id)):
            return JSONResponse(status_code=400,
                                content={
                                    "message": "Invalid : moderator id is not an integer"})

        hasError = False
        errorMessage = []


        if "email" in updated_user:
            email = updated_user["email"]
            updated_user["email"] = email.lower()
            if not validations.validate_email_syntax(updated_user["email"]):
                hasError = True
                errorMessage.append(errorsTypes.emailInvalid)

        if "password" in updated_user:
            (val,missings) =  validations.validate_password(updated_user["password"])
            if not val:
                hasError = True
                errorMessage.append(missings)
            updated_user["password"] = hashString(updated_user["password"])

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



        response = Database.updateUser(updated_user)

        return response


    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "message": "Error while updating moderator",
                "error": str(e)
            })


