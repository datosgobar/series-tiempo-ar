from urllib.parse import urlparse


class URLValidator:
    def is_valid(self, url):
        parsed = urlparse(url)
        return parsed.scheme and parsed.netloc
