from pydatajson import DataJson
from series_tiempo_ar.validations import validate_distribution
import pandas as pd
import numpy as np

catalog = DataJson("http://infra.datos.gob.ar/catalog/sspm/data.json")
identifier = "136.1"

distribution = catalog.get_distribution(identifier=identifier)
dataset = catalog.get_dataset(identifier=distribution['dataset_identifier'])

df = pd.read_csv(distribution['downloadURL'], parse_dates=['indice_tiempo']) \
    .set_index('indice_tiempo')

validate_distribution(df, catalog, dataset, distribution)
