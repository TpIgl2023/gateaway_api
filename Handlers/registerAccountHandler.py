from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from Core.Shared.DatabaseOperations import Database
from Services.authServices import hashString
from Services.authServices import validations
from Services.authServices import errorsTypes
from Services.authServices import createJwtToken

# OAuth2PasswordBearer for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def registerAccountHandler(name,email,password,phone):
    try :
        lowerCaseEmail = email.lower()
        #check if the fields are valid
        emailIsValid = validations.validate_email_syntax(lowerCaseEmail)
        passwordIsValid,_ = validations.validate_password(password)
        mobileIsValid = validations.validate_mobile(phone)
        nameIsValid = validations.validate_name(name) 
        errors = []
        if (emailIsValid & passwordIsValid & mobileIsValid & nameIsValid):
            usersResponse = Database.getAccountsWithFilter({"email":lowerCaseEmail})
            #check if email exists
            users = usersResponse["accounts"]
            if (len(users) == 0):
                # generating the token 
                token_data = {"email": lowerCaseEmail,"status": "status"}
                jwt_token = createJwtToken(token_data)
                password = hashString(password)
                user = {
                    "name": name,
                    "email": email,
                    "password": password,
                    "phone": phone
                }
                Database.createUser(user)
                del user["password"]
                response = JSONResponse(
                    content={"success":True,"message":"User created succesfully","user":user},
                    headers={"Authorization": f"Bearer {jwt_token}"}
                    )

                response.set_cookie(key="Authorization", value=jwt_token,httponly=True)
                return response
            else:
                return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "message":"This Email is already used"
                })
        else :
            passwordValid,passwordErrors = validations.validate_password(password)
            if(not validations.validate_email_syntax(email)):
                errors.append(errorsTypes.emailInvalid)
            if(not validations.validate_name(name)):
                errors.append(errorsTypes.nameInvalid)
            if(not passwordValid):
                errors.append(passwordErrors)
            if(not validations.validate_mobile(phone)):
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
                "message":"error while registering user. got an Exception",
                "error": str(e)
            }
        )
        

