import pandas as pd


class CSVReader:
    def __init__(self, distribution):
        self.distribution = distribution

    def read(self):
        download_url = self.distribution["downloadURL"]
        return pd.read_csv(download_url)
