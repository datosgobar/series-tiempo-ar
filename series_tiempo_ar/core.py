#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Módulo principal de series-tiempo-ar

Contiene una extensión del objeto pydatajson.DataJson con funcionalidades
adicionales para el manejo de datos y metadatos de catálogos con series de
tiempo.

Esta extensión está orientada a proveer una capa de abstracción que facilite:

    1. La implementación sistemática de rutinas de ETL para la compilación de
        series de tiempo desde fuentes semi-estructuradas.
    2. La validación y utilización programática de series de tiempo publicadas
        según la especificación del Perfil de Metadatos de la Política de
        Apertura de Datos de la Administración Pública Nacional de Argentina.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement

from pydatajson import DataJson

from series_tiempo_ar.readers.csv_reader import CSVReader
from series_tiempo_ar.readers.readers import get_distribution_generation_method
from series_tiempo_ar.readers.text_file_reader import (
    generate_ts_distribution_from_text_file,
)
from series_tiempo_ar.time_series_validator import TimeSeriesValidator
from .paths import SCHEMAS_DIR

DEFAULT_CATALOG_SCHEMA_FILENAME = "catalog.json"


class TimeSeriesDataJson(DataJson):
    """Métodos para trabajar con catálogos de series de tiempo en data.json."""

    def __init__(
        self,
        catalog=None,
        schema_filename=None,
        schema_dir=None,
        default_values=None,
        validator_class=TimeSeriesValidator,
        catalog_format=None,
    ):
        schema_filename = schema_filename or DEFAULT_CATALOG_SCHEMA_FILENAME
        schema_dir = schema_dir or SCHEMAS_DIR

        super(TimeSeriesDataJson, self).__init__(
            catalog=catalog,
            schema_filename=schema_filename,
            schema_dir=schema_dir,
            default_values=default_values,
            validator_class=validator_class,
            catalog_format=catalog_format,
        )

        self.generate_distribution_ids()

    def validate_time_series_catalog(self):
        errors = self.validator.get_catalog_errors(self)

        return {"status": "OK" if not errors else "ERROR", "errors": errors}

    # pylint: disable=W0613
    def load_ts_distribution(
        self,
        identifier,
        catalog_id=None,
        is_text_file=None,
        is_excel_file=None,
        is_csv_file=None,
        file_source=None,
    ):
        distribution = self.get_distribution(identifier)
        method = get_distribution_generation_method(distribution)

        # se genera a partir de un archivo de texto con parámetros
        if is_text_file or method == "text_file":
            return generate_ts_distribution_from_text_file(
                self, identifier, catalog_id, file_source=file_source
            )

        # se lee a partir de un CSV que cumple con la especificación
        if is_csv_file or method == "csv_file":
            return CSVReader(distribution, self.verify_ssl, file_source).read()

        raise NotImplementedError("{} no se puede leer".format(identifier))
