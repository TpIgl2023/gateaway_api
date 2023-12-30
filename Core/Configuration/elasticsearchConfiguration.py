from elasticsearch import Elasticsearch
import Core.Environment.elasticsearchEnv as env

# Create Elasticsearch client with default 'elastic' credentials
es = Elasticsearch(
    [env.ELASTICSEARCH_SERVICE_URL],
    basic_auth=(env.ELASTICSEARCH_USERNAME, env.ELASTICSEARCH_PASSWORD),
    # ca_certs=env.ELASTICSEARCH_CACERAT_PATH,
    # verify_certs=True
)


# Test the connection
if es.ping():
    print("Connected to Elasticsearch")
else:
    raise Exception("Connection to Elasticsearch failed")
