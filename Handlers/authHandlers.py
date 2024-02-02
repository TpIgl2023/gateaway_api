from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from Services.authServices import createJwtToken , hashString , validations , errorsTypes
from Core.Shared.DatabaseOperations import Database

# OAuth2PasswordBearer for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def loginAccountHandler(email, password):
    try:
        password = hashString(password)

        upperCaseEmail = email.lower()

        usersResponse = await Database.getAccountsWithFilter({"email":upperCaseEmail})

        # Check if the user exists
        if (usersResponse["message"] == "Accounts retrieved successfully"):
            users = usersResponse["accounts"]
            if len(users) != 0:
                for user in users:
                    if user["password"] == password:
                        del user["password"]
                        token_data = {"id": user["id"],"status": user["status"]}

                        jwt_token = createJwtToken(token_data)
                        response = JSONResponse(
                            content={"success":True,"user":user, "token" : jwt_token},
                            headers={"Authorization": f"Bearer {jwt_token}"},
                            )

                        response.set_cookie(key="Authorization", value=jwt_token,httponly=True)
                        return response
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message":"Invalid email or password"
            })
    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={
                "message": "Error while authenticating user",
                "error": str(e)
            })



async def registerUserAccountHandler(name, email, password, phone):
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
            print(users)
            if (len(users) == 0):
                # generating the token

                password = hashString(password)
                user = {
                    "name": name,
                    "email": lowerCaseEmail,
                    "password": password,
                    "phone": phone
                }
                dbResponse = await Database.createUser(user)

                if (dbResponse["message"] != "Account created successfully"):
                    raise Exception(dbResponse["message"])
                del user["password"]
                id = dbResponse["account"]["id"]
                token_data = {"id": str(id),"status": "user"}
                jwt_token = createJwtToken(token_data)

                response = JSONResponse(
                    content={"success": True, "message": "User created succesfully", "user": user},
                    headers={"Authorization": f"Bearer {jwt_token}"},
                )
                response.set_cookie(key="Authorization", value=jwt_token,httponly=True)
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


