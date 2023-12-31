import sys
import unittest
from unittest.mock import patch
from pathlib import Path

# Add the project directory to sys.path
project_directory = str(Path(__file__).resolve().parents[1])
sys.path.append(project_directory)


class TestElasticsearch(unittest.TestCase):

    @patch('Services.elasticsearchServices.index_article')
    def test_index_article(self, mock_index_article):
        # Arrange
        from Models.Article import Article
        article = Article(
            title='Elasticsearch in Python',
            text='This is a sample document for Elasticsearch indexing in Python.',
            keywords=['Elasticsearch', 'Python', 'sample', 'document', 'test'],
            authors=['John Doe', 'Jane Doe'],
        )
        article_id = 1

        # Act
        mock_index_article(article, article_id)
        # mock_elasticsearch_services.build_document_index(article)

        # Assert
        mock_index_article.assert_called_once_with(article, article_id)




if __name__ == '__main__':
    unittest.main()
