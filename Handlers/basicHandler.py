from starlette.responses import JSONResponse
import requests
import json

async def basicHandler():
    try:

        return {"Hello": "World"}


    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "message": "Error while sending request to database-service",
                                "error": str(e)
                            })