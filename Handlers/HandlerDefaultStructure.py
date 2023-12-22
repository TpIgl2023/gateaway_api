from starlette.responses import JSONResponse
import requests
import json

async def HANDLER_NAME():
    try:

        response = {
            "message": "Welcome to the API"
        }

        return response.json()
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error while sending request to database-service",
                "error": str(e)
            })