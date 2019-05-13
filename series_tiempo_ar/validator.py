from series_tiempo_ar import TimeSeriesDataJson
from series_tiempo_ar.validations import validate_distribution


def get_distribution_errors(catalog: TimeSeriesDataJson, distribution_id):
    try:
        distribution = catalog.get_distribution(distribution_id)
        df = catalog.load_ts_distribution(distribution_id)
        validate_distribution(df, catalog, None, distribution)
    except Exception as e:
        return [e]

    return []
