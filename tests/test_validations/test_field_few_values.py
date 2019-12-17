from unittest import TestCase


from series_tiempo_ar.custom_exceptions import FieldFewValuesError
from series_tiempo_ar.readers.csv_reader import CSVReader
from series_tiempo_ar.validations.csv_validations import (
    FieldViewValuesValidation,
    ValidationOptions,
)
from tests.helpers import csv_path


class TestFieldFewValues(TestCase):
    def setUp(self) -> None:
        self.distribution = {
            "field": [{"specialType": "time_index", "title": "indice_tiempo"}]
        }

    def test_validation_one_value_is_invalid(self):
        df = CSVReader(self.distribution, file_source=csv_path("few_values.csv")).read()
        with self.assertRaises(FieldFewValuesError):
            FieldViewValuesValidation(df).validate()

    def test_validation_with_custom_minimum_values(self):
        df = CSVReader(self.distribution, file_source=csv_path("few_values.csv")).read()

        FieldViewValuesValidation(
            df,
            None,
            None,
            options=ValidationOptions.create_with_defaults(minimum_values=0),
        ).validate()

    def test_validation_with_custom_max_too_small_proportion(self):
        df = CSVReader(self.distribution, file_source=csv_path("few_values.csv")).read()

        # Siempre es válido
        options = ValidationOptions.create_with_defaults(max_too_small_proportion=1.01)
        FieldViewValuesValidation(df, options=options).validate()
