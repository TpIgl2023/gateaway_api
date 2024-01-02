from fastapi import APIRouter, Request
import Handlers.articlesHandlers as articles_handler


articlesRouter = APIRouter()



@articlesRouter.post("/create")
async def upload_article_handler(request: Request):
    return await articles_handler.upload_article_handler(request)

