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

from .paths import SCHEMAS_DIR

DEFAULT_CATALOG_SCHEMA_FILENAME = "catalog.json"


class TimeSeriesDataJson(DataJson):
    """Métodos para trabajar con catálogos de series de tiempo en data.json."""

    def __init__(self, catalog=None, schema_filename=None, schema_dir=None,
                 default_values=None):
        schema_filename = schema_filename or DEFAULT_CATALOG_SCHEMA_FILENAME
        schema_dir = schema_dir or SCHEMAS_DIR

        super(TimeSeriesDataJson, self).__init__(
            catalog=catalog, schema_filename=schema_filename,
            schema_dir=schema_dir, default_values=default_values
        )
