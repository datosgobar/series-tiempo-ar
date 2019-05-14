#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Módulo con métodos para hacer validaciones"""

# pylint: disable=W0614
# pylint: disable=W0401
from series_tiempo_ar.validations.csv_validations import *
from series_tiempo_ar.validations.xlsx_validations import *


def validate_distribution(df, catalog, _dataset_meta, distrib_meta, _=None):
    # validaciones sólo de metadatos
    validate_field_id(df, distrib_meta, catalog)
    validate_no_repeated_fields(df, distrib_meta, catalog)
    validate_no_repeated_titles(df, distrib_meta, catalog)
    validate_no_repeated_descriptions(df, distrib_meta, catalog)
    validate_no_repeated_fields_in_distribution(df, distrib_meta, catalog)

    # validaciones de headers
    validate_field_title(df, distrib_meta, catalog)
    validate_title_length(df, distrib_meta, catalog)

    # validaciones de los valores de las series
    validate_missing_fields(df, distrib_meta, catalog)
    validate_values_are_numeric(df, distrib_meta, catalog)
    validate_distribution_null_series_amount(df, distrib_meta, catalog)
    validate_field_few_values(df, distrib_meta, catalog)
    validate_df_shape(df, distrib_meta, catalog)

    # deprecada: queda cubierta por `validate_distribution_null_series_amount`
    # validate_missing_values(df)


def validate_distribution_scraping(
    xl, worksheet, headers_coord, headers_value, distrib_meta, force_ids=True
):
    if force_ids:
        validate_header_cell_field_id(xl, worksheet, headers_coord, headers_value)
    else:
        validate_header_cell_field_id_or_blank(
            xl, worksheet, headers_coord, headers_value
        )

    validate_distinct_scraping_start_cells(distrib_meta)


def get_distribution_errors(catalog, distribution_id):
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
