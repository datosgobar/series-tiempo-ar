import io

import pandas as pd
import requests


class CSVReader:
    def __init__(self, distribution, verify_ssl=False):
        self.distribution = distribution
        self.verify_ssl = verify_ssl

    def read(self):
        download_url = self.distribution["downloadURL"]

        data = requests.get(download_url, verify=self.verify_ssl).content
        file_source = io.BytesIO(data)

        file_source.seek(0)
        try:
            return pd.read_csv(file_source, encoding="utf8")
        except UnicodeDecodeError:
            file_source.seek(0)
            return pd.read_csv(file_source, encoding="latin1")
