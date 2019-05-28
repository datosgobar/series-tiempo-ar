from unittest import TestCase

from tests.helpers import read_data_json


class ValidationsTests(TestCase):
    def test_valid_catalog(self):
        catalog = read_data_json("valid_catalog.json")
        validation = catalog.validate_catalog()

        self.assertEqual(validation["status"], "OK")

    def test_invalid_catalog(self):
        catalog = read_data_json("repeated_field_id.json")
        validation = catalog.validate_catalog()

        self.assertEqual(validation["status"], "ERROR")

    def test_invalid_format_catalog(self):
        catalog = read_data_json("missing_dataset_title.json")
        validation = catalog.validate_catalog()

        self.assertEqual(validation["status"], "ERROR")

    def test_missing_field_identifier(self):
        catalog = read_data_json("missing_dataset_title.json")
        validation = catalog.validate_catalog()

        self.assertEqual(validation["status"], "ERROR")
