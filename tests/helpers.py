import os

from series_tiempo_ar import TimeSeriesDataJson
from tests import SAMPLES_DIR


def read_data_json(file_name):
    return TimeSeriesDataJson(os.path.join(SAMPLES_DIR, file_name))


def csv_path(file_name):
    return os.path.join(SAMPLES_DIR, file_name)
