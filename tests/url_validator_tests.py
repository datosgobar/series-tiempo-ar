from unittest import TestCase

from series_tiempo_ar.utils.url_validator import URLValidator


class URLValidatorTests(TestCase):
    def test_valid_url(self):
        url = "http://google.com"
        self.assertTrue(URLValidator(url).is_valid())

    def test_invalid_url(self):
        url = "not an url"
        self.assertFalse(URLValidator(url).is_valid())

    def test_validate_file(self):
        url = "/path/to/a/file.csv"
        self.assertFalse(URLValidator(url).is_valid())
