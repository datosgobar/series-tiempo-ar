from unittest import TestCase

from series_tiempo_ar.custom_exceptions import FieldTitleTooLongError
from series_tiempo_ar.readers.csv_reader import CSVReader
from series_tiempo_ar.validations.csv_validations import (
    TitleLengthValidation,
    ValidationOptions,
)
from tests.helpers import csv_path


class TestTitleLengthValidation(TestCase):
    def setUp(self) -> None:
        self.distribution = {
            "field": [{"specialType": "time_index", "title": "indice_tiempo"}],
            "identifier": "test_id",
        }

    def test_too_long_title(self):
        df = CSVReader(
            self.distribution,
            file_source=csv_path("70_character_long_column_title.csv"),
        ).read()
        with self.assertRaises(FieldTitleTooLongError):
            TitleLengthValidation(df).validate()

    def test_custom_length(self):
        df = CSVReader(
            self.distribution,
            file_source=csv_path("70_character_long_column_title.csv"),
        ).read()
        options = ValidationOptions.create_with_defaults(max_field_title_len=71)
        TitleLengthValidation(df, options=options).validate()
