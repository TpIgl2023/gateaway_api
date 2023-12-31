from fastapi import APIRouter
from Handlers.basicHandler import basicHandler
#from Core.Configuration.elasticsearchConfiguration import es


root_router = APIRouter()
'''
@root_router.get("/")
async def handle_pdf():
    # Indexing a document
    index_name = 'my_index'
    document = {
        'title': 'Elasticsearch in Python',
        'content': 'This is a sample document for Elasticsearch indexing in Python.',
        'keywords': ['Elasticsearch', 'Python', 'sample', 'document', 'test']
    }

    # Index the document
    es.index(index=index_name, document=document, id=1)

    # Refresh the index to make the document available for search immediately (optional)
    es.indices.refresh(index=index_name)

    # String to search
    search_string = 'indexing'

    # Search across all fields in all indices
    search_query = {
        'query': {
            'multi_match': {
                'query': search_string,
                'fields': ['*'],
                'type': 'best_fields'
            }
        }
    }

    # Search the index
    results = es.search(index=index_name, body=search_query)

    # Print search results
    print("Search Results:")
    for hit in results['hits']['hits']:
        print(f"Document ID: {hit['_id']}, Score: {hit['_score']}")
        print(hit['_source'])
        print("\n")

    return await basicHandler()'''

