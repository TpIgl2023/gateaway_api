import concurrent
from datetime import datetime

from starlette import status
from starlette.responses import JSONResponse
from Core.Environment.pdfServiceEnv import PDF_SERVICE_API_KEY, PDF_SERVICE_API_URL
from Core.Environment.databaseServiceEnv import DATABASE_SERVICE_API_KEY, DATABASE_API_URL
from Services.adminServices import is_url, is_int, isModerator, getDriveFilesId, GoogleDriveHandler, processMultiplePdf
from Core.Shared.DatabaseOperations import Database
import requests
import json

from Services.authServices import validations, createJwtToken, hashString, errorsTypes


async def ExtractFromPdf(URL):
    try:
        if not is_url(URL):
            return JSONResponse(
                status_code=200,
                content={
                    "success": False,
                    "message": "URL is not valid"})

        if GoogleDriveHandler.isDriveLink(URL):
            # Extract the id of the google drive folder
            folderId = GoogleDriveHandler.extractFolderId(URL)

            # Use the ID to extract the id of the files
            ids = getDriveFilesId(folderId)

            # Extract the text from the files
            downloadLinkArray = []
            for id in ids:
                downloadLinkArray.append(GoogleDriveHandler.extractGoogleDownloadLink(id))

            response = {"success": True,
                        "sourceType":"drive",
                        "downloadLinks": downloadLinkArray}

            return response

        else:
            headers = {'x-api-key': PDF_SERVICE_API_KEY}

            params = {'URL': URL}

            response = requests.get(PDF_SERVICE_API_URL, headers=headers, params=params)

            response =  response.json()

            response["sourceType"] = "fileLink"
            response["success"] = True

            if 'publishingDate' in response:
                date_string = response['publishingDate']
                try:
                    # Convert the string to a dictionary
                    if date_string is not None:
                        date_dict = json.loads(date_string)
                        if 'formatted_date' in date_dict:
                            # Parse the date string
                            date_object = datetime.strptime(date_dict['formatted_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                            # Format the date as required
                            formatted_date = date_object.strftime('%Y-%m-%d')
                            # Update the dictionary
                            response['publishingDate'] = formatted_date
                    else:
                        response['publishingDate'] = ""
                except Exception as e:
                    response['publishingDate'] = ""
                    print("Error: Unable to parse date string.")


            return response



    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Error while extracting data from PDF",
                "error": str(e)
            })

async def ExtractFromPdfs(URLs):
    try:
        if not isinstance(URLs, list):
            return JSONResponse(
                status_code=400,
                content={"message": "URLs is not valid"})

        headers = {'x-api-key': PDF_SERVICE_API_KEY}

        params = URLs

        response = requests.get(PDF_SERVICE_API_URL, headers=headers, params=params)

        return response.json()

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Error while extracting data from PDF",
                "error": str(e)
            })


async def getAllModerators():
    try:
        response = await Database.getAllModerators()
        response =  response.json()
        if response["message"] != "Moderators retrieved successfully":
            return JSONResponse(status_code=500,
                content={
                    "success": False,
                    "message": "Error while getting moderators",
                    "error": response["message"]
                })
        response["success"] = True
        moderators = response["moderators"]
        for moderator in moderators:
            del moderator["password"]
        response["moderators"] = moderators

        return response
    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "success": False,
                "message": "Error while getting moderators",
                "error": str(e)
            })


async def adminRestrictedPageHandler():
    try:
        return {"Hello": "Admin !"}
    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "success": False,
                "message": "Error while sending request to database-service",
                "error": str(e)
            })


async def deleteModerator(id):
    try:
        isMod = await isModerator(id)

        if isMod == "No moderators found":
            return JSONResponse(status_code=404,
                content={
                    "success":False,
                    "message": "No moderators found"
                })

        if type(isMod) != bool:
            return isMod

        if not isMod:
            return JSONResponse(status_code=400,
                content={
                    "success": False,
                    "message": "User is not a moderator"
                })

        # Delete the user
        response = await Database.deleteUser(str(id))

        if response["message"] == "Account deleted successfully":
            response["success"] = True
        else:
            response["success"] = False

        return response
    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "success": False,
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
            usersResponse = await Database.getAccountsWithFilter({"email": lowerCaseEmail})
            # check if email exists
            users = usersResponse["accounts"]
            if (len(users) == 0):
                # generating the token

                password = hashString(password)
                user = {
                    "name": name,
                    "email": lowerCaseEmail,
                    "password": password,
                    "phone": phone
                }
                dbResponse = await Database.createUser(user, accountType="moderator")
                del user["password"]
                if (dbResponse["message"] != "Account created successfully"):
                    raise dbResponse["message"]
                id = dbResponse["account"]["id"]
                token_data = {"id": str(id), "status": "moderator"}
                jwt_token = createJwtToken(token_data)
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
                "success": False,
                "message": "error while registering user. got an Exception",
                "error": str(e)
            }
        )


async def editModeratorAccountHandler(updated_user):
    try:

        if "id" not in updated_user:
            return JSONResponse(status_code=400,
                                content={
                                    "success":False,
                                    "message": "Missing moderator id"})

        id = updated_user["id"]

        isMod = await isModerator(id)

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
                                    "success":False,
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



        response = await Database.updateUser(updated_user)

        response["success"] = True



        return response


    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "success": False,
                "message": "Error while updating moderator",
                "error": str(e)
            })


async def extractFromDrive(URL):
    try:
        if not is_url(URL):
            return JSONResponse(
                status_code=400,
                content={"message": "URL is not valid"})


        # Extract the id of the google drive folder
        folderId = GoogleDriveHandler.extractFolderId(URL)

        # Use the ID to extract the id of the files
        ids = getDriveFilesId(folderId)

        # Extract the text from the files
        downloadLinkArray = []
        for id in ids:
            downloadLinkArray.append(GoogleDriveHandler.extractGoogleDownloadLink(id))

        extractedArticles = []
        nbArticles = 0

        for downloadLink in downloadLinkArray:
            try :
                article = await ExtractFromPdf(downloadLink)
                extractedArticles.append(article)
                print(article)
                nbArticles += 1
            except Exception as e:
                print(e)
                pass


        response = {
            "success": True,
            "nbArticlesExtracted": nbArticles,
            "articles": extractedArticles
        }

        print(response)

        return response


    except Exception as e:
       return JSONResponse(
            status_code=500,
            content={
                "message": "Error while extracting data from PDF",
                "error": str(e)
            })


async def extractDownloadLinksFromDrive(URL):
    try:
        if not is_url(URL):
            return JSONResponse(
                status_code=400,
                content={"message": "URL is not valid"})

        # Extract the id of the google drive folder
        folderId = GoogleDriveHandler.extractFolderId(URL)

        # Use the ID to extract the id of the files
        ids = getDriveFilesId(folderId)

        # Extract the text from the files
        downloadLinkArray = []
        for id in ids:
            downloadLinkArray.append(GoogleDriveHandler.extractGoogleDownloadLink(id))

        response = {"success": True,
                    "downloadLinks": downloadLinkArray}

        return response



    except Exception as e:
       return JSONResponse(
            status_code=500,
            content={
                "message": "Error while extracting data from PDF",
                "error": str(e)
            })




