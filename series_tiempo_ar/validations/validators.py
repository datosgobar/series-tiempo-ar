#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Módulo con métodos para hacer validaciones"""

from series_tiempo_ar.custom_exceptions import TimeSeriesError
from series_tiempo_ar.validations.xlsx_validations import (
    validate_header_cell_field_id,
    validate_header_cell_field_id_or_blank,
    validate_distinct_scraping_start_cells,
)
from .csv_validations import ValidationOptions, BaseValidation


class Validator:
    def __init__(self, catalog, distrbution_id, validations, options=None):
        self.catalog = catalog
        self.distribution_id = distrbution_id
        self.validations = validations
        self.options = options

    def get_distribution_errors(self):
        """Ejecuta todas las validaciones y devuelve los errores (excepciones)
        levantadas
        """
        distribution = self.catalog.get_distribution(self.distribution_id)
        df = self.catalog.load_ts_distribution(self.distribution_id)
        errors = []
        for validation in self.validations:
            try:
                validation(df, distribution, self.catalog, self.options).validate()
            except TimeSeriesError as e:
                errors.append(e)

        return errors

    def validate_distribution(self, df=None):
        """Ejecuta validaciones. Lanza una excepción de tipo TimeSeriesError
        ante un error
        """
        distribution = self.catalog.get_distribution(self.distribution_id)
        df = (
            df
            if df is not None
            else self.catalog.load_ts_distribution(self.distribution_id)
        )

        for validation in self.validations:
            validation(df, distribution, self.catalog).validate()


# Entry points "legacy"


def validate_distribution(df, catalog, _dataset_meta, distrib_meta, _=None):
    Validator(
        catalog, distrib_meta["identifier"], BaseValidation.__subclasses__()
    ).validate_distribution(df)


def get_distribution_errors(catalog, distribution_id, options=None):
    return Validator(
        catalog, distribution_id, BaseValidation.__subclasses__(), options
    ).get_distribution_errors()


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
