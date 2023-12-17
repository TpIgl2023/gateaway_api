from starlette.responses import JSONResponse

async def basic_handler():
    try:
        response = {
            "Hello": "World"
        }
        return JSONResponse(content=response)
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "message": "Error while processing the PDF",
                                "error": str(e)
                            })