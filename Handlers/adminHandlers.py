from starlette.responses import JSONResponse



async def adminRestrictedPageHandler():
    try:
        return {"Hello": "Admin !"}
    except Exception as e:
        return JSONResponse(status_code=500,
            content={
                "message": "Error while sending request to database-service",
                "error": str(e)
            })