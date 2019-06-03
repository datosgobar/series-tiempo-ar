import pandas as pd


class CSVReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        return pd.read_csv(self.file_path)
