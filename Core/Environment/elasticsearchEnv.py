import os

# Elasticsearch environment variables
PORT = 1234
ELASTICSEARCH_SERVICE_URL = 'https://localhost:' + str(PORT)
ELASTICSEARCH_CACERAT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../Files/elasticsearch_http_cacerat.crt')
ELASTICSEARCH_USERNAME = 'elastic'
ELASTICSEARCH_PASSWORD = 'VflWwT43SVHyUrgBNmlb'

ARTICLE_INDEX = 'articles'