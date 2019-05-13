from unittest import TestCase

from series_tiempo_ar.custom_exceptions import FieldIdRepetitionError
from series_tiempo_ar.validator import get_distribution_errors
from tests.helpers import read_data_json


class GetErrorsTests(TestCase):
    def test_get_errors_of_valid_distribution_empty(self):
        data_json = read_data_json("data.json")
        errors = get_distribution_errors(data_json, "125.1")
        self.assertFalse(errors)

    def test_get_errors_repeated_field_id_catalog(self):
        data_json = read_data_json("repeated_field_id.json")
        errors = get_distribution_errors(data_json, "125.1")
        self.assertIn(FieldIdRepetitionError, map(lambda x: x.__class__, errors))
