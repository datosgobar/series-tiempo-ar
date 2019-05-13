import os

from pydatajson import DataJson

from series_tiempo_ar import TimeSeriesDataJson

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")


def read_data_json(file_name):
    return TimeSeriesDataJson(os.path.join(SAMPLES_DIR, file_name))
