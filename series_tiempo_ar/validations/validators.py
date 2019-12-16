#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Módulo con métodos para hacer validaciones"""

# pylint: disable=W0614
# pylint: disable=W0401
from series_tiempo_ar.custom_exceptions import TimeSeriesError
from series_tiempo_ar.validations.xlsx_validations import *
from . import csv_validations


class Validator:
    def __init__(self, catalog, distrbution_id, validations=None):
        self.catalog = catalog
        self.distribution_id = distrbution_id
        self.validations = validations

    def get_distribution_errors(self):
        distribution = self.catalog.get_distribution(self.distribution_id)
        df = self.catalog.load_ts_distribution(self.distribution_id)
        errors = []
        for validation in self._get_validations():
            try:
                validation(df, distribution, self.catalog).validate()
            except TimeSeriesError as e:
                errors.append(e)

        return errors

    def validate_distribution(self, df=None):
        for validation in self._get_validations():
            distribution = self.catalog.get_distribution(self.distribution_id)
            df = (
                df
                if df is not None
                else self.catalog.load_ts_distribution(self.distribution_id)
            )

            validation(df, distribution, self.catalog).validate()

    def _get_validations(self):
        if self.validations:
            return self.validations

        return csv_validations.BaseValidation.__subclasses__()


def validate_distribution(df, catalog, _dataset_meta, distrib_meta, _=None):
    Validator(catalog, distrib_meta["identifier"]).validate_distribution(df)


def get_distribution_errors(catalog, distribution_id):
    return Validator(catalog, distribution_id).get_distribution_errors()


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
