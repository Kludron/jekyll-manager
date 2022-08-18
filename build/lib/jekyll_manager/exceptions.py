# List of all exception types used in jekyll-manager
class JekyllRootException(Exception):
    def __init__(self, message):
        super().__init__(message)

