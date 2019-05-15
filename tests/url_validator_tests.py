from unittest import TestCase

from series_tiempo_ar.utils.url_validator import URLValidator


class URLValidatorTests(TestCase):
    def test_valid_url(self):
        url = "http://google.com"
        self.assertTrue(URLValidator().is_valid(url))

    def test_invalid_url(self):
        url = 'not an url'
        self.assertFalse(URLValidator().is_valid(url))

    def test_validate_file(self):
        url = '/path/to/a/file.csv'
        self.assertFalse(URLValidator().is_valid(url))
