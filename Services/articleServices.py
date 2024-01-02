from Core.Exceptions.databaseException import DatabaseException
from Models.Article import Article
from Core.Configuration.databaseConfiguration import articlesDatabaseClient


def _fields_rename_for_database(article: dict):
    article["resume"] = article["abstract"]
    article.pop("abstract")

    article["pdfUrl"] = article["URL"]
    article.pop("URL")

    article["references"] = article["bibliography"]
    article.pop("bibliography")

    article["publishDate"] = article["publishingDate"]
    article.pop("publishingDate")


async def _upload_article_to_database(article: Article):
    article_json = article.__dict__()

    # Rename the fields to match the database
    _fields_rename_for_database(article_json)

    response = await articlesDatabaseClient.post("/create", json=article_json)
    if response.status_code != 200:
        raise DatabaseException(response.json()["message"], response.status_code)

    return response.json()["article"]


# TODO: complete this function
async def upload_article(article: Article):
    # Upload the article to the database
    uploaded_article = await _upload_article_to_database(article)

    return uploaded_article
