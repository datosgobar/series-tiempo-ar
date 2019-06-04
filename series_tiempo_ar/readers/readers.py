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

import pandas as pd


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
