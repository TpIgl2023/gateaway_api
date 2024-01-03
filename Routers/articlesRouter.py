from fastapi import APIRouter, Request
import Handlers.articlesHandlers as articles_handler


articlesRouter = APIRouter()


# TODO: add jwt and admin authentication middleware
@articlesRouter.post("/")
async def upload_article_handler(request: Request):
    return await articles_handler.upload_article_handler(request)


# TODO: add jwt and mod authentication middleware
@articlesRouter.put("/{article_id}")
async def modify_article_handler(article_id: int, request: Request):
    return await articles_handler.modify_article_handler(request, article_id)

