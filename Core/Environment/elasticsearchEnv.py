import os

# Elasticsearch environment variables
PORT = 32769
ELASTICSEARCH_SERVICE_URL = 'https://localhost:' + str(PORT)
ELASTICSEARCH_CACERAT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../Files/elasticsearch_http_cacerat.crt')
ELASTICSEARCH_USERNAME = 'elastic'
ELASTICSEARCH_PASSWORD = 'BY-VmV-NAKs66AB2YK=e'

ARTICLE_INDEX = 'articles'