#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Módulo con métodos para hacer validaciones"""

# pylint: disable=W0614
# pylint: disable=W0401
from series_tiempo_ar.custom_exceptions import TimeSeriesError
from series_tiempo_ar.validations.xlsx_validations import *
from . import csv_validations


def _is_validation_function(func):
    return (
        callable(func)
        and func.__module__ == csv_validations.__name__
        and func.__name__[0] != "_"
    )


CSV_VALIDATIONS = [
    x
    for x in [getattr(csv_validations, x) for x in dir(csv_validations)]
    if _is_validation_function(x)
]


def validate_distribution(df, catalog, _dataset_meta, distrib_meta, _=None):
    for validation in CSV_VALIDATIONS:
        validation(df, distrib_meta, catalog)


def get_distribution_errors(catalog, distribution_id):
    distribution = catalog.get_distribution(distribution_id)
    df = catalog.load_ts_distribution(distribution_id)
    errors = []
    for validation in CSV_VALIDATIONS:
        try:
            validation(df, distribution, catalog)
        except TimeSeriesError as e:
            errors.append(e)

    return errors


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
