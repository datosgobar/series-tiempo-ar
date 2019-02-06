#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Funciones auxiliares para leer distintas distribuciones de series de tiempo

Permite leer (online o local):
    1. Distribuciones CSV que cumplen la especificación oficial
    2. Distribuciones a parsear desde un TXT o CSV con formato de panel
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import os
import pandas as pd
import arrow

from .helpers import freq_iso_to_pandas, find_encoding, find_dialect
from .helpers import fix_time_index
from pydatajson.time_series import get_distribution_time_index


def load_ts_distribution(catalog, identifier, catalog_id=None,
                         is_text_file=None, is_excel_file=None,
                         is_csv_file=None, file_source=None):
    """Carga en un DataFrame una distribución de series de tiempo.

    Permite leer (online o local):
        1. Distribuciones CSV que cumplen la especificación oficial
        2. Distribuciones a parsear desde un TXT o CSV con formato de panel
    """
    distribution = catalog.get_distribution(identifier)
    method = get_distribution_generation_method(distribution)

    # se genera a partir de un archivo de texto con parámetros
    if is_text_file or method == "text_file":
        return generate_ts_distribution_from_text_file(
            catalog, identifier, catalog_id)

    # se scrapea a partir de un Excel con parámetros (usando otro proyecto)
    elif is_excel_file or method == "excel_file":
        print("Usar el scraper de series de tiempo.")
        return None

    # se lee a partir de un CSV que cumple con la especificación
    elif is_csv_file or method == "csv_file":
        file_source = file_source or distribution["downloadURL"]
        time_index = get_distribution_time_index(distribution)
        return pd.read_csv(
            file_source, index_col=time_index,
            parse_dates=[time_index],
            date_parser=lambda x: arrow.get(x, "YYYY-MM-DD").datetime
            # encoding="utf-8"
        )

    else:
        raise NotImplementedError("{} no se puede leer".format(identifier))


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
            distribution.get("scrapingFileURL")):
        return "text_file"

    # se scrapea a partir de un Excel con parámetros (usando otro proyecto)
    elif (not distribution.get("downloadURL") and
          _is_excel_file(distribution.get("scrapingFileURL"))):
        return "excel_file"

    # se lee a partir de un CSV que cumple con la especificación
    elif distribution.get("downloadURL"):
        return "csv_file"

    else:
        raise NotImplementedError("{} no se puede leer".format(
            distribution["identifier"]))


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


def generate_ts_distribution_from_text_file(catalog, identifier,
                                            catalog_id=None):
    distribution = catalog.get_distribution(identifier)
    frequency = catalog.get_distribution_time_index_frequency(distribution)
    catalog_id = catalog_id or catalog.get("identifier")

    # parámetros de lectura del archivo de texto
    sep = distribution["scrapingFileSeparator"]
    encoding = distribution["scrapingFileEncoding"]
    path = distribution["scrapingFileURL"]
    time_format = distribution["scrapingFileTimeFormat"]
    fields = _get_fields(
        distribution["scrapingFileTimeField"],
        distribution["scrapingFileIdsField"],
        distribution["scrapingFileValuesField"]
    )

    # lectura del archivo de texto según los parámetros del catálogo
    df_panel = pd.read_csv(
        path, sep=sep,
        names=fields["default_names"] if fields["ordinal"] else None,
        encoding=encoding,
        converters={fields["series_id_field"]: str}
    )

    # transforma los ids de las series del catálogo, eliminando el catalog_id
    # prependeado para volverlos únicos dentro de la base completa, ahora los
    # ids de las series son los mismos que el archivo original del publicador
    series = {
        ts["id"].replace(catalog_id + "-", ""): ts["title"]
        for ts in catalog.get_time_series(distribution_identifier=identifier)
    }

    # transforma dataframe de panel simple en distribución de series de tiempo
    df_series = get_series_df_from_panel(
        df_panel, series, frequency,
        time_format=time_format,
        time_field=fields["time_field"],
        series_id_field=fields["series_id_field"],
        values_field=fields["values_field"]
    )

    return df_series


def _get_fields(time_field, series_id_field, values_field):
    fields = {}

    if (str(time_field).isdigit() and
        str(series_id_field).isdigit() and
            str(values_field).isdigit()):
        fields["ordinal"] = True
        default_names = {
            "serie_id": series_id_field,
            "indice_tiempo": time_field,
            "valor": values_field
        }
        sorted_default_names = sorted(
            list(default_names.iteritems()), key=lambda tup: tup[1])
        fields["default_names"] = [tup[0] for tup in sorted_default_names]
        fields["time_field"] = "indice_tiempo"
        fields["series_id_field"] = "serie_id"
        fields["values_field"] = "valor"

    else:
        fields["ordinal"] = False
        fields["default_names"] = ["serie_id", "indice_tiempo", "valor"]
        fields["time_field"] = time_field
        fields["series_id_field"] = series_id_field
        fields["values_field"] = values_field

    return fields


def get_series_df_from_panel(
        df_panel, series, time_index_freq,
        time_format="%Y-%m-%d", time_field="indice_tiempo",
        series_id_field="serie_id", values_field="valor"):
    """Convierte tabla con id, fecha y valor en distribución de TS.

    Args:
        df_panel (pd.DataFrame): Tabla con columnas de id de series, fecha
            y valor de observaciones.
        series (dict): Donde los keys son "field_id" de series y los values
            son "field_title" de las series.
        time_field (str): Campo que tiene la fecha.
        time_format (str): Formato en el que hay que parsear la fecha.
        series_id_field (str): Campo que tiene el id de la serie.
        values_field (str): Campo que tiene los valores de las observaciones.

    return: pd.DataFrame
    """

    # parsea el campo de fechas al tipo datetime
    df_panel[time_field] = pd.to_datetime(
        df_panel[time_field], format=time_format)

    # se queda solo con las series elegidas
    df = df_panel[df_panel[series_id_field].isin(series.keys())]

    # construye un período continuo para el índice de tiempo, el más largo
    period_range = pd.date_range(
        min(df.indice_tiempo),
        max(df.indice_tiempo),
        freq=freq_iso_to_pandas(time_index_freq))

    def get_single_series(serie_id):
        time_values = df[df[series_id_field] == serie_id][time_field]
        time_period = pd.PeriodIndex(
            time_values,
            freq=freq_iso_to_pandas(time_index_freq, "end"))
        time_index = time_period.to_timestamp()

        values = list(df[df[series_id_field] == serie_id][values_field])

        time_index, values = fix_time_index(
            time_index, values,
            freq_iso_to_pandas(time_index_freq, "end"))

        return pd.Series(index=pd.to_datetime(time_index), data=values)

    data = {
        series[serie_id]: get_single_series(serie_id)
        for serie_id in series
    }

    df_series = pd.DataFrame(index=period_range, data=data)

    return df_series
