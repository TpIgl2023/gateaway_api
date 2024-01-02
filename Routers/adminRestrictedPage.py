from fastapi import APIRouter, Depends
from Handlers.adminRestrictedPageHandler import adminRestrictedPageHandler
from Middlwares.AuthProtectionMiddlewares import isAdminProtected

adminRouter = APIRouter()

@adminRouter.get("/")
async def handlePage(user: str = Depends(isAdminProtected)):
    return await adminRestrictedPageHandler()

