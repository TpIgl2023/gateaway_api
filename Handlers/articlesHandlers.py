from fastapi import Request
from starlette.responses import JSONResponse

from Core.Exceptions.databaseException import DatabaseException
from Models.Article import Article
from Services.articleServices import upload_article, modify_article, get_article_by_id, delete_article, search_articles_by_query


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


async def get_article_by_id_handler(article_id: int):
    try:
        # Get the article data from the request
        article = await get_article_by_id(article_id)

        if article is None:
            return JSONResponse(status_code=404,
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


async def search_articles_handler(request: Request):
    try:
        # Get the article data from the request
        query = request.query_params.get('query')

        # search the articles
        articles = await search_articles_by_query(query)

        if articles is not None:
            return JSONResponse(status_code=200,
                                content={
                                    "message": "Articles retrieved successfully",
                                    "articles": articles
                                })
        else:
            return JSONResponse(status_code=404,
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