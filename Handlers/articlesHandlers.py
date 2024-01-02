from fastapi import Request
from starlette.responses import JSONResponse

from Core.Exceptions.databaseException import DatabaseException
from Models.Article import Article
from Services.articleServices import upload_article


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
                                "error": str(e)
                            })
    except Exception as e:
        print("exception:")
        print(e)
        return JSONResponse(status_code=400,
                            content={
                                "message": "Error while creating article",
                                "error": str(e)
                            })