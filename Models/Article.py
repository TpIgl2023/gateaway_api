class Article:

    def __init__(
            self,
            title = None,
            abstract = None,
            authors = None,
            institutions = None,
            keywords = None,
            text = None,
            URL = None,
            bibliography = None,
            publishingDate = None
    ):
        self.title = title
        self.abstract = abstract
        self.authors = authors
        self.institutions = institutions
        self.keywords = keywords
        self.text = text
        self.URL = URL
        self.bibliography = bibliography
        self.publishingDate = publishingDate

    def __str__(self):

        return f"Title: {self.title}\n" \
               f"Abstract: {self.abstract}\n" \
               f"Authors: {self.authors}\n" \
               f"Institutions: {self.institutions}\n" \
               f"Keywords: {self.keywords}\n" \
               f"URL: {self.URL}\n" \
               f"Bibliography: {self.bibliography}\n" \
               f"Publishing Date: {self.publishingDate}"

    def __dict__(self):
        return {
            "title": self.title,
            "abstract": self.abstract,
            "authors": self.authors,
            "institutions": self.institutions,
            "keywords": self.keywords,
            "text": self.text,
            "URL": self.URL,
            "bibliography": self.bibliography,
            "publishingDate": self.publishingDate
        }


