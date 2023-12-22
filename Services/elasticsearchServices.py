from Core.Configuration.elasticsearchConfiguration import es
from Core.Environment.elasticsearchEnv import ARTICLE_INDEX
from Models.Article import Article


def index_article(article: Article, article_id: int):
    # Building the article index
    index = _build_document_index(article)

    # Index the document
    es.index(index=ARTICLE_INDEX, document=index, id=article_id)

    # Refresh the index to make the document available for search immediately (optional)
    es.indices.refresh(index=index)


def _build_document_index(article: Article):
    index = article.__dict__()

    # declare fields to be removed from the index
    to_remove = ['abstract', 'institutions', 'keywords', 'URL', 'bibliography', 'publishingDate']

    # remove fields from the index
    for field in to_remove:
        if field in index:
            index.pop(field)

    # index is ready
    return index

