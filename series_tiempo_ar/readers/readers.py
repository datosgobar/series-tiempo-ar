#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Funciones auxiliares para leer distintas distribuciones de series de tiempo

Permite leer (online o local):
    1. Distribuciones CSV que cumplen la especificación oficial
    2. Distribuciones a parsear desde un TXT o CSV con formato de panel
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement

import io

import arrow
import pandas as pd
import requests
from pydatajson.time_series import get_distribution_time_index

from series_tiempo_ar.utils.url_validator import URLValidator
from .text_file_reader import generate_ts_distribution_from_text_file


def load_ts_distribution(
    catalog,
    identifier,
    catalog_id=None,
    is_text_file=None,
    is_excel_file=None,
    is_csv_file=None,
    file_source=None,
    verify_ssl=False,
):
    """Carga en un DataFrame una distribución de series de tiempo.

    Permite leer (online o local):
        1. Distribuciones CSV que cumplen la especificación oficial
        2. Distribuciones a parsear desde un TXT o CSV con formato de panel
    """
    distribution = catalog.get_distribution(identifier)
    method = get_distribution_generation_method(distribution)

    # se genera a partir de un archivo de texto con parámetros
    if is_text_file or method == "text_file":
        return generate_ts_distribution_from_text_file(catalog, identifier, catalog_id)

    # se scrapea a partir de un Excel con parámetros (usando otro proyecto)
    if is_excel_file or method == "excel_file":
        print("Usar el scraper de series de tiempo.")
        return None

    # se lee a partir de un CSV que cumple con la especificación
    if is_csv_file or method == "csv_file":
        file_source = file_source or distribution["downloadURL"]
        if URLValidator(file_source).is_valid():
            data = requests.get(file_source, verify=verify_ssl).content
            file_source = io.BytesIO(data)
        else:
            file_source = open(file_source, "rb")
        time_index = get_distribution_time_index(distribution)

        date_parsers = [
            lambda x: arrow.get(x, "YYYY-MM-DD").datetime,
            lambda x: arrow.get(x, "YYYY-MM").datetime,
            lambda x: arrow.get(x, "YYYY").datetime,
        ]

        for date_parser in date_parsers:
            try:
                return read_csv(file_source, time_index, date_parser)
            except arrow.parser.ParserError:
                continue
        raise Exception("El formato de fecha no es válido.")

    raise NotImplementedError("{} no se puede leer".format(identifier))


def read_csv(url_or_filepath, time_index, date_parser):
    return read_csv_with_encoding(
        url_or_filepath,
        index_col=time_index,
        parse_dates=[time_index],
        date_parser=date_parser,
    )


def read_csv_with_encoding(url_or_filepath, *args, **kwargs):
    url_or_filepath.seek(0)
    try:
        return pd.read_csv(url_or_filepath, *args, **kwargs, encoding="utf8")
    except UnicodeDecodeError:
        url_or_filepath.seek(0)
        return pd.read_csv(url_or_filepath, *args, **kwargs, encoding="latin1")


def get_ts_distributions_by_method(catalog, method=None):
    """Devuelve las dist. de series de tiempo generables por X método.

    Args:
        catalog (TimeSeriesDataJson): Catálogo con series de tiempo.
        method (list or str): Lista o uno de 'text_file',
            'csv_file', 'excel_file'
    """
    if not method:
        return catalog.get_distributions(only_time_series=True)

    # los métodos se pueden pasar por lista, o un solo método por string
    distributions = []
    if isinstance(method, str):
        method = [method]

    for distribution in catalog.get_distributions(only_time_series=True):
        if get_distribution_generation_method(distribution) in method:
            distributions.append(distribution)

    return distributions


def get_distribution_generation_method(distribution):
    # se genera a partir de un archivo de texto con parámetros
    if not distribution.get("downloadURL") and _is_text_file(
        distribution.get("scrapingFileURL")
    ):
        return "text_file"

    # se scrapea a partir de un Excel con parámetros (usando otro proyecto)
    if not distribution.get("downloadURL") and _is_excel_file(
        distribution.get("scrapingFileURL")
    ):
        return "excel_file"

    # se lee a partir de un CSV que cumple con la especificación
    if distribution.get("downloadURL"):
        return "csv_file"

    raise NotImplementedError("{} no se puede leer".format(distribution["identifier"]))


def _is_text_file(path_or_url):
    if not path_or_url:
        return False
    extension = path_or_url.split(".")[-1].lower()
    return extension in ["txt", "csv"]


def _is_excel_file(path_or_url):
    if not path_or_url:
        return False
    extension = path_or_url.split(".")[-1].lower()
    return extension in ["xls", "xlsx"]
