from unittest import TestCase

from series_tiempo_ar.custom_exceptions import (
    FieldIdRepetitionError,
    FieldDescriptionRepetitionError,
)
from series_tiempo_ar.validations import get_distribution_errors
from tests.helpers import read_data_json


class GetErrorsTests(TestCase):
    def test_get_errors_of_valid_distribution_empty(self):
        data_json = read_data_json("data.json")
        errors = get_distribution_errors(data_json, "125.1")
        self.assertFalse(errors)

    def test_get_errors_repeated_field_id_catalog(self):
        data_json = read_data_json("repeated_field_id.json")
        errors = get_distribution_errors(data_json, "125.1")
        self.assertIn(FieldIdRepetitionError, [x.__class__ for x in errors])

    def test_multiple_errors(self):
        data_json = read_data_json("repeated_field_id_and_description.json")
        errors = get_distribution_errors(data_json, "125.1")
        error_classes = [x.__class__ for x in errors]
        self.assertIn(FieldIdRepetitionError, error_classes)
        self.assertIn(FieldDescriptionRepetitionError, error_classes)
