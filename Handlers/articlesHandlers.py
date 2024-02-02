from fastapi import Request
from starlette.responses import JSONResponse

from Core.Exceptions.databaseException import DatabaseException
from Models.Article import Article
from Services.articleServices import \
    upload_article, modify_article, \
    get_article_by_id, delete_article, \
    search_articles_by_query, \
    add_article_to_favorites, \
    remove_article_from_favorites, \
    get_user_favorites, \
    get_articles


async def upload_article_handler(request: Request):
    try:
        # Get the article data from the request
        article_dict = await request.json()
        # Create the article object
        article = Article.from_dict(article_dict)
        # upload the article to the database
        uploaded_article = await upload_article(article)

        return JSONResponse(status_code=200,
                            content={
                                "message": "Article created successfully",
                                "article": uploaded_article
                            })

    except DatabaseException as e:
        print("database exception:")
        print(e)
        return JSONResponse(status_code=e.status_code,
                            content={
                                "message": "Error while creating article",
                                "error": e.message
                            })
    except Exception as e:
        print("exception:")
        print(e)
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while creating article",
                                "error": str(e)
                            })


async def modify_article_handler(request: Request, article_id: int):
    try:
        # Get the article data from the request
        article_dict = await request.json()
        # modify the article
        modified_article = await modify_article(article_dict, article_id)

        return JSONResponse(status_code=200,
                            content={
                                "message": "Article created successfully",
                                "article": modified_article
                            })
    except DatabaseException as e:
        print("database exception:")
        print(e)
        return JSONResponse(status_code=e.status_code,
                            content={
                                "message": "Error while creating article",
                                "error": e.message
                            })
    except Exception as e:
        print("exception:")
        print(e)
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while creating article",
                                "error": str(e)
                            })


async def get_article_by_id_handler(article_id: int, user_id: str):
    try:
        # Get the article data from the request
        article = await get_article_by_id(article_id, user_id=int(user_id) if user_id is not None else None)

        if article is None:
            return JSONResponse(status_code=200,
                                content={
                                    "message": "Article not found",
                                    "article": {}
                                })
        else:

            return JSONResponse(status_code=200,
                                content={
                                    "message": "Article retrieved successfully",
                                    "article": article
                                })
    except DatabaseException as e:
        print("database exception:")
        print(e)
        return JSONResponse(status_code=e.status_code,
                            content={
                                "message": "Error while retrieving article",
                                "error": e.message
                            })
    except Exception as e:
        print("exception:")
        print(e)
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while retrieving article",
                                "error": str(e)
                            })


async def delete_article_handler(article_id: int):
    try:
        # Get the article data from the request
        await delete_article(article_id)

        return JSONResponse(status_code=200,
                            content={
                                "message": "Article deleted successfully",
                            })
    except DatabaseException as e:
        print("database exception:")
        print(e)
        return JSONResponse(status_code=e.status_code,
                            content={
                                "message": "Error while deleting article",
                                "error": e.message
                            })
    except Exception as e:
        print("exception:")
        print(e)
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while deleting article",
                                "error": str(e)
                            })


async def search_articles_handler(request: Request, user_id: str):
    try:
        # Get the article data from the request
        query = request.query_params.get('query')

        # search the articles
        articles = await search_articles_by_query(query, user_id=int(user_id) if user_id is not None else None)

        if articles is not None:
            return JSONResponse(status_code=200,
                                content={
                                    "message": "Articles retrieved successfully",
                                    "articles": articles
                                })
        else:
            return JSONResponse(status_code=200,
                                content={
                                    "message": "Articles not found",
                                    "articles": []
                                })
    except DatabaseException as e:
        print("database exception:")
        print(e)
        return JSONResponse(status_code=e.status_code,
                            content={
                                "message": "Error while retrieving articles",
                                "error": e.message
                            })
    except Exception as e:
        print("exception:")
        print(e)
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while retrieving articles",
                                "error": str(e)
                            })


async def add_article_to_favorite_handler(request: Request, user_id: str):
    try:
        # Get the article data from the request
        article_id = request.headers.get('article_id')

        # search the articles
        article = await add_article_to_favorites(int(user_id), int(article_id))

        if article is not None:
            return JSONResponse(status_code=200,
                                content={
                                    "message": "Article added to favorite successfully",
                                    "article": article
                                })
        else:
            return JSONResponse(status_code=200,
                                content={
                                    "message": "Article not found",
                                    "article": {}
                                })

    except DatabaseException as e:
        print(e)
        return JSONResponse(status_code=e.status_code,
                            content={
                                "message": "Error while adding article to favorite",
                                "error": e.message
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while adding article to favorite",
                                "error": str(e)
                            })


async def remove_article_from_favorite_handler(request: Request, user_id: str):
    try:
        # Get the article data from the request
        article_id = request.headers.get('article_id')

        # search the articles
        article = await remove_article_from_favorites(int(user_id), int(article_id))

        if article is not None:
            return JSONResponse(status_code=200,
                                content={
                                    "message": "Article removed from favorite successfully",
                                    "article": article
                                })
        else:
            return JSONResponse(status_code=200
                                ,
                                content={
                                    "message": "Article not found",
                                    "article": {}
                                })

    except DatabaseException as e:
        return JSONResponse(status_code=e.status_code,
                            content={
                                "message": "Error while removing article from favorite",
                                "error": e.message
                            })
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while removing article from favorite",
                                "error": str(e)
                            })


async def get_favorite_articles_handler(user_id: str):
    try:
        # search the articles
        articles = await get_user_favorites(int(user_id))

        if articles is not None:
            return JSONResponse(status_code=200,
                                content={
                                    "message": "Articles retrieved successfully",
                                    "articles": articles
                                })
        else:
            return JSONResponse(status_code=200
                                ,
                                content={
                                    "message": "Articles not found",
                                    "articles": []
                                })

    except DatabaseException as e:
        return JSONResponse(status_code=e.status_code,
                            content={
                                "message": "Error while retrieving articles",
                                "error": e.message
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while retrieving articles",
                                "error": str(e)
                            })


async def get_articles_handler(user_id: str = None):
    try:
        # search the articles
        articles = await get_articles(user_id=int(user_id) if user_id is not None else None)

        if articles is not None:
            return JSONResponse(status_code=200,
                                content={
                                    "message": "Articles retrieved successfully",
                                    "articles": articles
                                })
        else:
            return JSONResponse(status_code=200,
                                content={
                                    "message": "Articles not found",
                                    "articles": []
                                })

    except DatabaseException as e:
        return JSONResponse(status_code=e.status_code,
                            content={
                                "message": "Error while retrieving articles",
                                "error": e.message
                            })
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while retrieving articles",
                                "error": str(e)
                            })
