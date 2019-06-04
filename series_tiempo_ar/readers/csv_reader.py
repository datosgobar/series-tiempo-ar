import io
from contextlib import contextmanager

import pandas as pd
import requests


class CSVReader:
    def __init__(self, distribution, verify_ssl=False, file_source=None):
        self.distribution = distribution
        self.verify_ssl = verify_ssl
        self.file_source = file_source

    def read(self):
        with self.read_distribution() as f:
            try:
                return pd.read_csv(f, encoding="utf8")
            except UnicodeDecodeError:
                f.seek(0)
                return pd.read_csv(f, encoding="latin1")

    @contextmanager
    def read_distribution(self):
        if self.file_source:
            fd = open(self.file_source, "rb")
            try:
                yield fd
            finally:
                fd.close()
        else:
            data = requests.get(
                self.distribution["downloadURL"], verify=self.verify_ssl
            ).content
            file_source = io.BytesIO(data)
            try:
                yield file_source
            finally:
                file_source.close()
