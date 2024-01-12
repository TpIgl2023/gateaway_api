from fastapi import APIRouter, Request, Depends
import Handlers.articlesHandlers as articles_handler
from Middlwares.AuthProtectionMiddlewares import isAdminProtected, isModeratorProtected, isUserProtected, isUserAndModProtected

articlesRouter = APIRouter()


@articlesRouter.post("/")
async def upload_article(request: Request, user: str = Depends(isAdminProtected)):
    return await articles_handler.upload_article_handler(request)


@articlesRouter.post("/favorite")
async def favorite_article(request: Request, user: str = Depends(isUserProtected)):
    return await articles_handler.add_article_to_favorite_handler(request, user)


@articlesRouter.delete("/favorite")
async def unfavorite_article(request: Request, user: str = Depends(isUserProtected)):
    return await articles_handler.remove_article_from_favorite_handler(request, user)


@articlesRouter.get("/favorite")
async def get_user_favorites(user: str = Depends(isUserProtected)):
    return await articles_handler.get_favorite_articles_handler(user)


@articlesRouter.get("/all")
async def get_articles_by_ids(request: Request, user: str = Depends(isUserAndModProtected)):
    return await articles_handler.get_articles_handler(user)


@articlesRouter.put("/{article_id}")
async def modify_article(article_id: int, request: Request, user: str = Depends(isModeratorProtected)):
    return await articles_handler.modify_article_handler(request, article_id)


@articlesRouter.get("/{article_id}")
async def get_article_by_id(article_id: int, user: str = Depends(isUserAndModProtected)):
    return await articles_handler.get_article_by_id_handler(article_id, user)


@articlesRouter.delete("/{article_id}")
async def delete_article(article_id: int, user: str = Depends(isModeratorProtected)):
    return await articles_handler.delete_article_handler(article_id)


@articlesRouter.get("/")
async def get_articles(request: Request, user: str = Depends(isUserAndModProtected)):
    return await articles_handler.search_articles_handler(request, user)





