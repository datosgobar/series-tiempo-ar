from unittest import TestCase

from series_tiempo_ar.custom_exceptions import DistributionTooManyNullSeriesError
from series_tiempo_ar.readers.csv_reader import CSVReader
from series_tiempo_ar.validations.csv_validations import (
    DistributionNullSeriesValidation,
    ValidationOptions,
)
from tests.helpers import csv_path


class TestNullSeriesValidation(TestCase):
    def setUp(self) -> None:
        self.distribution = {
            "field": [{"specialType": "time_index", "title": "indice_tiempo"}],
            "identifier": "test_id",
        }

    def test_all_null_distribution_is_invalid(self):
        df = CSVReader(self.distribution, file_source=csv_path("all_null.csv")).read()
        with self.assertRaises(DistributionTooManyNullSeriesError):
            DistributionNullSeriesValidation(df, self.distribution, None).validate()

    def test_custom_null_proportion(self):
        df = CSVReader(self.distribution, file_source=csv_path("all_null.csv")).read()

        options = ValidationOptions.create_with_defaults(
            max_null_series_proportion=1.1
        )  # Se permite 100% null
        DistributionNullSeriesValidation(
            df, self.distribution, options=options
        ).validate()
