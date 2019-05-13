from series_tiempo_ar import TimeSeriesDataJson

# pylint: disable=W0401
# pylint: disable=W0614
from series_tiempo_ar.validations import *


def get_distribution_errors(catalog: TimeSeriesDataJson, distribution_id):
    distribution = catalog.get_distribution(distribution_id)
    df = catalog.load_ts_distribution(distribution_id)
    functions = [
        validate_field_id,
        validate_no_repeated_fields,
        validate_no_repeated_titles,
        validate_no_repeated_descriptions,
        validate_no_repeated_fields_in_distribution,
        validate_field_title,
        validate_title_length,
        validate_missing_fields,
        validate_values_are_numeric,
        validate_distribution_null_series_amount,
        validate_field_few_values,
        validate_df_shape,
    ]
    errors = []
    for validation in functions:
        try:
            validation(df, distribution, catalog)
        except Exception as e:
            errors.append(e)

    return errors
