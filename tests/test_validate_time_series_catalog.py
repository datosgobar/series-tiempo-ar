from unittest import TestCase

from tests.helpers import read_data_json


class ValidateTimeSeriesCatalogTests(TestCase):
    def test_validate_time_series_catalog(self):
        catalog = read_data_json("valid_catalog.json")
        validation = catalog.validate_time_series_catalog()

        self.assertEqual(validation["status"], "OK")

    def test_invalid_catalog(self):
        catalog = read_data_json("repeated_field_id.json")
        validation = catalog.validate_time_series_catalog()

        self.assertEqual(validation["status"], "ERROR")

    def test_valid_catalog_has_empty_errors(self):
        catalog = read_data_json("valid_catalog.json")
        validation = catalog.validate_time_series_catalog()

        self.assertFalse(validation["errors"])

    def test_invalid_catalog_has_errors(self):
        catalog = read_data_json("repeated_field_id.json")
        validation = catalog.validate_time_series_catalog()

        self.assertTrue(validation["errors"]["125.1"])
