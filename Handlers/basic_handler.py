from starlette.responses import JSONResponse
import requests
import json

async def basic_handler():
    try:


        url = "https://database-service-t3er.onrender.com/accounts/create"
        headers = {
            'x-api-key': 'ad188b63-b8e0-4c34-8781-df6cc17ae132',
            'User-Agent': 'Apidog/1.0.0 (https://apidog.com)',
            'Content-Type': 'application/json',
            'account_type': 'user'
        }

        data = {
            "name": "Soapiane",
            "email": "user@email.com",
            "password": "user",
            "phone": "+21359047526"
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)

        return response.json()
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "message": "Error while sending request to database-service",
                                "error": str(e)
                            })