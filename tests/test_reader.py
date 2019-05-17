import os
from unittest import TestCase

from series_tiempo_ar.readers import read_csv

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")


class CSVReaderTests(TestCase):
    def test_read_csv_latin1(self):
        df = read_csv(
            open(os.path.join(SAMPLES_DIR, "daily_periodicity_latin1.csv"), "rb"),
            "índice_tiempo",
            None,
        )
        self.assertTrue(list(df.columns))
