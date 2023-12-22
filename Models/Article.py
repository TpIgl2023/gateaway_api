class Article:

    def __init__(self):
        self.title = None
        self.abstract = None
        self.authors = None
        self.institutions = None
        self.keywords = None
        self.text = None
        self.URL = None
        self.bibliography = None
        self.publishingDate = None

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


