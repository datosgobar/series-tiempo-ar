import io

import pandas as pd
import requests
from pydatajson.time_series import get_distribution_time_index


class CSVReader:
    def __init__(self, distribution, verify_ssl=False, file_source=None):
        self.distribution = distribution
        self.verify_ssl = verify_ssl
        self.file_source = file_source

    def read(self):
        with self.read_distribution() as f:
            try:
                return self.read_csv(f, encoding="utf8")
            except UnicodeDecodeError:
                f.seek(io.SEEK_SET)
                return self.read_csv(f, encoding="latin1")

    def read_distribution(self):
        if self.file_source:
            return open(self.file_source, "rb")

        data = requests.get(
            self.distribution["downloadURL"], verify=self.verify_ssl
        ).content
        return io.BytesIO(data)

    def read_csv(self, buffer, encoding):
        time_index = get_distribution_time_index(self.distribution)
        return pd.read_csv(
            buffer, index_col=time_index, parse_dates=[time_index], encoding=encoding
        )
