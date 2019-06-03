from unittest import TestCase

from series_tiempo_ar.readers.csv_reader import CSVReader
from tests.helpers import csv_path, read_data_json


class CSVReaderTests(TestCase):
    def test_returns_a_data_frame(self):
        data_json = read_data_json("valid_catalog.json")
        distribution = data_json.get_distributions()[0]
        df = CSVReader(distribution).read()

        self.assertIn("title1", list(df.columns))
