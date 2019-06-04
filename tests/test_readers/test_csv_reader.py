from unittest import TestCase

from series_tiempo_ar.readers.csv_reader import CSVReader
from tests.helpers import csv_path, read_data_json


class CSVReaderTests(TestCase):
    def test_returns_a_data_frame(self):
        df = self._read_csv("valid_catalog.json")
        self.assertIn("title1", list(df.columns))

    def test_read_latin1_distribution(self):
        df = self._read_csv("daily_periodicity_latin1.json")
        self.assertIn("tasas_interés_call", list(df.columns))

    def test_read_from_file_source(self):
        data_json = read_data_json("daily_periodicity_latin1.json")
        distribution = data_json.get_distributions()[0]
        path = csv_path("sample_data.csv")
        df = CSVReader(distribution, file_source=path).read()
        self.assertIn("title1", list(df.columns))

    def test_data_frame_has_time_index(self):
        df = self._read_csv("valid_catalog.json")
        self.assertEqual(str(df.index[0].date()), "2000-01-01")

    def test_read_year_only_distribution(self):
        df = self._read_csv("year_only_distribution.json")
        self.assertEqual(str(df.index[0].date()), "2000-01-01")

    def _read_csv(self, filename):
        data_json = read_data_json(filename)
        distribution = data_json.get_distributions()[0]
        df = CSVReader(distribution).read()
        return df
