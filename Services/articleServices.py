from Core.Exceptions.databaseException import DatabaseException
from Models.Article import Article
from Core.Configuration.databaseConfiguration import articlesDatabaseClient
from Services.elasticsearchServices import index_article, remove_article_from_index, search_articles
import json


def _fields_rename_for_database(article: dict):
    if "abstract" in article:
        article["resume"] = article["abstract"]
        article.pop("abstract")

    if "URL" in article:
        article["pdfUrl"] = article["URL"]
        article.pop("URL")

    if "bibliography" in article:
        article["references"] = article["bibliography"]
        article.pop("bibliography")

    if "publishingDate" in article:
        article["publishDate"] = article["publishingDate"]
        article.pop("publishingDate")


async def _upload_article_to_database(article: Article):
    article_json = article.__dict__()

    # Rename the fields to match the database
    _fields_rename_for_database(article_json)

    response = await articlesDatabaseClient.post("/create", json=article_json)
    if response.status_code != 200:
        raise DatabaseException(response.json(), response.status_code)

    return response.json()["article"]


async def upload_article(article: Article):
    # Upload the article to the database
    uploaded_article = await _upload_article_to_database(article)

    # Index the article
    index_article(article, uploaded_article["id"])

    return uploaded_article


async def _update_article_in_database(updated_info: dict, article_id: int):
    # Rename the fields to match the database
    _fields_rename_for_database(updated_info)

    # Include the id in the json
    updated_info["id"] = article_id

    response = await articlesDatabaseClient.put("/update", json=updated_info)
    if response.status_code != 200:
        raise DatabaseException(response.json(), response.status_code)

    return response.json()["article"]


async def modify_article(updated_info: dict, article_id: int):
    # Update the article in the database
    updated_article = await _update_article_in_database(updated_info, article_id)
    # Update the article index in elasticsearch
    index_article(Article.from_dict(updated_article), updated_article["id"])

    return updated_article


async def _remove_article_from_database(article_id: int):
    response = await articlesDatabaseClient.delete(
        "/delete",
        headers=articlesDatabaseClient.headers.update({
            "id": str(article_id)
        }))
    if response.status_code != 200:
        raise DatabaseException(response.json(), response.status_code)


async def delete_article(article_id: int):
    # Remove the article from the database
    await _remove_article_from_database(article_id)

    # Remove the article from the index
    remove_article_from_index(article_id)


async def get_article_by_id(article_id: int, user_id: int = None):
    response = await articlesDatabaseClient.get(
        "/" + str(article_id),
        headers=articlesDatabaseClient.headers.update({
            "user_id": str(user_id)
        }) if user_id is not None else articlesDatabaseClient.headers
    )
    if response.status_code == 404:
        return None
    if response.status_code != 200:
        raise DatabaseException(response.json(), response.status_code)

    return response.json()["article"]


async def search_articles_by_query(query: str, user_id: str = None):
    # Search the articles in elastic search
    total, articles_ids_string = search_articles(query)

    if total == 0:
        return None

    # Convert the articles ids to a list of integers
    articles_ids = [int(article_id) for article_id in articles_ids_string]

    # Get the articles from the database
    response = await articlesDatabaseClient.request(
        method="GET",
        url="/getArticlesByIds",
        content=json.dumps({
            "ids": articles_ids
        }),
        headers=articlesDatabaseClient.headers.update({
            "user_id": str(user_id)
        }) if user_id is not None else articlesDatabaseClient.headers
    )

    articles = response.json()["articles"]

    if len(articles) == 0:
        return None
    return articles


async def add_article_to_favorites(user_id: int, article_id: int):
    response = await articlesDatabaseClient.post(
        "/addFavorite",
        headers=articlesDatabaseClient.headers.update({
            "user_id": str(user_id),
            "article_id": str(article_id)
        }),
    )
    if response.status_code != 200:
        raise DatabaseException(response.json(), response.status_code)

    return response.json()["article"]


async def remove_article_from_favorites(user_id: int, article_id: int):
    response = await articlesDatabaseClient.delete(
        "/removeFavorite",
        headers=articlesDatabaseClient.headers.update({
            "user_id": str(user_id),
            "article_id": str(article_id)
        }),
    )
    if response.status_code != 200:
        raise DatabaseException(response.json(), response.status_code)

    return response.json()["article"]


async def get_user_favorites(user_id: int):
    response = await articlesDatabaseClient.get(
        "/getFavorites",
        headers=articlesDatabaseClient.headers.update({
            "user_id": str(user_id)
        }),
    )
    if response.status_code != 200:
        raise DatabaseException(response.json(), response.status_code)

    if len(response.json()["articles"]) == 0:
        return None

    return response.json()["articles"]


async def get_articles(user_id: int = None):
    response = await articlesDatabaseClient.get(
        "/getArticles",
        headers=articlesDatabaseClient.headers.update({
            "user_id": str(user_id)
        }) if user_id is not None else articlesDatabaseClient.headers
    )
    if response.status_code != 200:
        raise DatabaseException(response.json(), response.status_code)

    if len(response.json()["articles"]) == 0:
        return None

    return response.json()["articles"]
