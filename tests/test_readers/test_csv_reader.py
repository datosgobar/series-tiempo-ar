from unittest import TestCase

from series_tiempo_ar.readers.csv_reader import CSVReader
from tests.helpers import csv_path


class CSVReaderTests(TestCase):

    def test_returns_a_data_frame(self):
        csv_file = csv_path('sample_data.csv')

        df = CSVReader(csv_file).read()

        self.assertIn('title1', list(df.columns))
