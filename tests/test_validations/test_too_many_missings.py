from unittest import TestCase

from series_tiempo_ar.custom_exceptions import FieldTooManyMissingsError
from series_tiempo_ar.readers.csv_reader import CSVReader
from series_tiempo_ar.validations.csv_validations import (
    MissingValuesValidation,
    ValidationOptions,
)
from tests.helpers import csv_path


class TestTooManyMissings(TestCase):
    def setUp(self) -> None:
        self.distribution = {
            "field": [{"specialType": "time_index", "title": "indice_tiempo"}],
            "identifier": "test_id",
        }

    def test_full_serie_ok(self):
        df = CSVReader(
            self.distribution, file_source=csv_path("sample_data.csv")
        ).read()
        MissingValuesValidation(df).validate()

    def test_single_null_not_ok_with_custom_option(self):
        df = CSVReader(
            self.distribution, file_source=csv_path("single_null.csv")
        ).read()
        options = ValidationOptions.create_with_defaults(max_missing_proportion=0.2)
        with self.assertRaises(FieldTooManyMissingsError):
            MissingValuesValidation(df, options=options).validate()
