from typing import Dict

from fastapi import APIRouter, Depends, Header

from Handlers.adminHandlers import adminRestrictedPageHandler, ExtractFromPdf, getAllModerators, deleteModerator, \
    registerModeratorAccountHandler, editModeratorAccountHandler, extractFromDrive, extractDownloadLinksFromDrive
from Middlwares.AuthProtectionMiddlewares import isAdminProtected
from Models.RequestsModels import registerRequest , ExtractionRequest

adminRouter = APIRouter()

@adminRouter.get("/")
async def handlePage(user: str = Depends(isAdminProtected)):
    return await adminRestrictedPageHandler()

@adminRouter.post("/extract")
async def extractPDF(login_data: ExtractionRequest, user: str = Depends(isAdminProtected)):
    email = login_data.URL
    return await ExtractFromPdf(email)

@adminRouter.post("/extract/multiple")
async def extractMultiplePDF(login_data: ExtractionRequest, user: str = Depends(isAdminProtected)):
    url = login_data.URL
    return await extractFromDrive(url)

@adminRouter.post("/extract/drive")
async def extractDownloadLinks(login_data: ExtractionRequest, user: str = Depends(isAdminProtected)):
    url = login_data.URL
    return await extractDownloadLinksFromDrive(url)


@adminRouter.get("/moderator")
async def getModerators(user: str = Depends(isAdminProtected)):
    return await getAllModerators()

@adminRouter.delete("/moderator")
async def deleteMod(id : int = Header(None),user: str = Depends(isAdminProtected)):
    return await deleteModerator(id)

@adminRouter.post("/moderator")
async def registerModeratorAccount(register_data: registerRequest, user: str = Depends(isAdminProtected)):
    name = register_data.name
    email = register_data.email
    password = register_data.password
    phone = register_data.phone
    return await registerModeratorAccountHandler(name, email, password, phone)

@adminRouter.put("/moderator")
async def editModeratorAccount(data: Dict, user: str = Depends(isAdminProtected)):

    return await editModeratorAccountHandler(data)