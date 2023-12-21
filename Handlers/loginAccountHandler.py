from fastapi import  status
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from Core.createJwtToken import createJwtToken
from Core.getAccountsWithFilter import getAccountsWithFilter
from Core.hashString import hashString


# OAuth2PasswordBearer for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def loginAccountHandler(email, password):
    try:
        password = hashString(password)

        upperCaseEmail = email.lower()

        usersResponse = getAccountsWithFilter({"email":upperCaseEmail})

        # Check if the user exists
        if (usersResponse["message"] == "Accounts retrieved successfully"):
            users = usersResponse["accounts"]
            if len(users) != 0:
                for user in users:
                    if user["password"] == password:
                        token_data = {"email": user["email"],"status": user["status"]}
                        jwt_token = createJwtToken(token_data)
                        response = JSONResponse(
                            content={"success":True,"user":user},
                            headers={"Authorization": f"Bearer {jwt_token}"},
                            )
                        del user["password"]

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