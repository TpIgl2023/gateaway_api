from Core.Configuration.elasticsearchConfiguration import es as elasticsearch
from Core.Environment.elasticsearchEnv import ARTICLE_INDEX
from Models.Article import Article


def index_article(article: Article, article_id: int):
    # Building the article index
    index = _build_document_index(article)

    elasticsearch.index(index=ARTICLE_INDEX, document=index, id=article_id)

    # Refresh the index to make the document available for search immediately (optional)
    elasticsearch.indices.refresh(index=ARTICLE_INDEX)


def _build_document_index(article: Article):
    index = article.__dict__()

    # declare fields to be removed from the index
    to_remove = ['abstract', 'institutions', 'pdfUrl', 'bibliography', 'publishingDate']

    # remove fields from the index
    for field in to_remove:
        if field in index:
            index.pop(field)

    # index is ready
    return index


def search_articles(query: str):
    # Search across all fields in all indices
    search_query = {
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['*'],
                'type': 'best_fields'
            }
        },
        # 'min_score': 0.2,
    }

    # Search the index
    search_results = elasticsearch.search(index=ARTICLE_INDEX, body=search_query)

    # Get the number of results
    total = search_results['hits']['total']['value']

    # Extract document IDs and create an array
    articles_ids = [hit['_id'] for hit in search_results['hits']['hits']]

    # return the results
    return total, articles_ids


def remove_article_from_index(article_id: int):
    # Remove the article from the index
    elasticsearch.delete(index=ARTICLE_INDEX, id=article_id)
