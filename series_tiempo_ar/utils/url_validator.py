from urllib.parse import urlparse


class URLValidator:
    def __init__(self, url):
        self.url = url

    def is_valid(self):
        parsed = urlparse(self.url)
        return parsed.scheme and parsed.netloc
