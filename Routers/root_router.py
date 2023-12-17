from fastapi import APIRouter
from Handlers.basic_handler import basic_handler


root_router = APIRouter()

@root_router.get("/")
async def handle_pdf():
    return await basic_handler()

