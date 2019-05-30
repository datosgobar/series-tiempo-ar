from unittest import TestCase

from series_tiempo_ar.readers import load_ts_distribution
from series_tiempo_ar.validations.csv_validations import validate_values_are_numeric
from tests.helpers import read_data_json


class ValuesAreNumericTests(TestCase):
    def test_validation_only_considers_columns_in_df(self):
        catalog = read_data_json("distribution_missing_column_in_data.json")
        distrib_meta = catalog.get_distribution(identifier="125.1")
        df = load_ts_distribution(catalog, "125.1")
        validate_values_are_numeric(df, distrib_meta, catalog)
