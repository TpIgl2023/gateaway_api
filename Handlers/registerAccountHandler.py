from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from Core.createJwtToken import createJwtToken
from Core.getAccountsWithFilter import getAccountsWithFilter
from Core.hashString import hashString
from Core.registrationExceptions import validate_email_syntax
from Core.registrationExceptions import validate_password
from Core.registrationExceptions import validate_mobile
from Core.registrationExceptions import validate_name

# OAuth2PasswordBearer for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def registerAccountHandler(email, name, password, phone):
    try :
        password = hashString(password)
        lowerCaseEmail = email.lower()
        #check if email and password and phone are valid
        emailIsValid = validate_email_syntax(lowerCaseEmail)
        passwordIsValid = validate_password(password)
        mobileIsValid = validate_mobile(phone)
        nameIsValid = validate_name(name)
        if (emailIsValid & passwordIsValid & mobileIsValid & nameIsValid):
            usersResponse = getAccountsWithFilter({"email":lowerCaseEmail})
            #check if email exists
            users = usersResponse["accounts"]
            if (len(users) == 0):
                #generating the token 
                token_data = {"email": lowerCaseEmail,"status": "status"}
                jwt_token = createJwtToken(token_data)
                user = {
                    #! idk how to generate the id
                    "id" : 31,
                    "name": name,
                    "email": email,
                    "password": password,
                    "phone": phone
                }
                response = JSONResponse(
                    content={"success":True,"user":user},
                    headers={"Authorization": f"Bearer {jwt_token}"},
                    )
                del password
                response.set_cookie(key="Authorization", value=jwt_token,httponly=True)
                return response
            else:
                JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "message":"This Email is already used"
                })
        else :
            cpt = 0
            if(not emailIsValid):
                message =+ "email, "
                cpt =+ 1
            if(not nameIsValid):
                message =+ "name, "
                cpt =+1
            if(not passwordIsValid):
                message =+ "password, "
                cpt =+1
            if (not mobileIsValid):
                phone =+ "phone, "
                cpt =+1
            if (cpt == 1):
                message =+ "chunk is not valid ! please review it then retry"
            else:
                message =+ "chunks are not valid ! please review them then retry"
            JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": message
            })

    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={
                "message":"error while registering user",
                "error": str(e)
            }
        )
        

