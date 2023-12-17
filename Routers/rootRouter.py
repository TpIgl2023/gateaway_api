from fastapi import APIRouter
from Handlers.basicHandler import basicHandler


rootRouter = APIRouter()

@rootRouter.get("/")
async def handle_pdf():
    return await basicHandler()

