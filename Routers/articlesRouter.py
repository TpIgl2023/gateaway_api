from fastapi import APIRouter, Request, Depends
import Handlers.articlesHandlers as articles_handler
from Middlwares.AuthProtectionMiddlewares import isAdminProtected, isModeratorProtected


articlesRouter = APIRouter()


@articlesRouter.post("/")
async def upload_article_handler(request: Request, user: str = Depends(isAdminProtected)):
    return await articles_handler.upload_article_handler(request)


@articlesRouter.put("/{article_id}")
async def modify_article_handler(article_id: int, request: Request, user: str = Depends(isModeratorProtected)):
    return await articles_handler.modify_article_handler(request, article_id)


@articlesRouter.get("/{article_id}")
async def get_article_by_id_handler(article_id: int):
    return await articles_handler.get_article_by_id_handler(article_id)


@articlesRouter.delete("/{article_id}")
async def delete_article_handler(article_id: int, user: str = Depends(isModeratorProtected)):
    return await articles_handler.delete_article_handler(article_id)


@articlesRouter.get("/")
async def get_articles_handler(request: Request):
    return await articles_handler.search_articles_handler(request)

