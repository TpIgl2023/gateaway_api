from fastapi import APIRouter
from Handlers.basicHandler import basicHandler


rootRouter = APIRouter()

@rootRouter.get("/")
async def basicHandler():
    return { "message": "Hello World"}

