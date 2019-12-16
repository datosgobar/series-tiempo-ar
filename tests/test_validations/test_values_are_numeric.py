from unittest import TestCase

from series_tiempo_ar.validations.csv_validations import ValuesAreNumericValidation
from tests.helpers import read_data_json


class ValuesAreNumericTests(TestCase):
    def test_validation_only_considers_columns_in_df(self):
        catalog = read_data_json("distribution_missing_column_in_data.json")
        distrib_meta = catalog.get_distribution(identifier="125.1")
        df = catalog.load_ts_distribution("125.1")
        ValuesAreNumericValidation(df, distrib_meta, catalog).validate()
