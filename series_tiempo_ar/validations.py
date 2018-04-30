#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Módulo con métodos para hacer validaciones"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import pandas as pd
import numpy as np
import arrow
import string
from six import text_type
from pandas.api.types import is_numeric_dtype
from dateutil.parser import parse as parse_time

import series_tiempo_ar.custom_exceptions as ce
from .helpers import freq_iso_to_pandas

MINIMUM_VALUES = 2
MAX_MISSING_PROPORTION = 0.999
MIN_TEMPORAL_FRACTION = 10
MAX_FIELD_TITLE_LEN = 60


def _assert_repeated_value(field_name, field_values, exception):
    fields = pd.Series([field[field_name] for field in field_values])
    field_dups = fields[fields.duplicated()].values
    if not len(field_dups) == 0:
        raise exception(repeated_fields=field_dups)


def validate_future_time(df):
    # No debe haber fechas futuras
    for time_value in df.index:
        time_value = arrow.get(time_value.year, time_value.month,
                               time_value.day)
        if not time_value.year <= arrow.now().year:
            iso_time_value = time_value.isoformat()
            iso_now = arrow.now().isoformat()
            raise ce.TimeIndexFutureTimeValueError(iso_time_value, iso_now)


def validate_field_few_values(df):
    # Las series deben tener una cantidad mínima de valores
    for field in df.columns:
        positive_values = len(df[field][df[field].notnull()])
        if not positive_values >= MINIMUM_VALUES:
            raise ce.FieldFewValuesError(
                field, positive_values, MINIMUM_VALUES
            )


def validate_field_title(df):
    # Los titulos de los campos deben tener caracteres ASCII + "_"
    valid_field_chars = "abcdefghijklmnopqrstuvwxyz0123456789_"
    for field in df.columns:
        if "unnamed" in field.lower():
            raise ce.InvalidFieldTitleError(
                field, is_unnamed=True
            )
        for char in field:
            if char not in valid_field_chars:
                raise ce.InvalidFieldTitleError(
                    field, char=char, valid_field_chars=valid_field_chars
                )


def validate_field_id(distrib_meta):
    # Los ids de los campos deben tener caracteres ASCII + "_"
    special_chars = "_-."
    valid_field_chars = string.ascii_letters + string.digits + special_chars
    for field_id in [field["id"] for field in distrib_meta["field"]
                     if "id" in field]:
        for char in field_id:
            if char not in valid_field_chars:
                raise ce.InvalidFieldIdError(
                    field_id, char, valid_field_chars
                )


def validate_title_length(df):
    # Los nombres de los campos tienen que tener un máximo de caracteres
    for field in df.columns:
        if len(field) > MAX_FIELD_TITLE_LEN:
            raise ce.FieldTitleTooLongError(
                field, len(field), MAX_FIELD_TITLE_LEN
            )


def validate_missing_values(df):
    # Las series deben tener una proporción máxima de missings
    for field in df.columns:
        total_values = len(df[field])
        positive_values = len(df[field][df[field].notnull()])
        missing_values = total_values - positive_values
        missing_values_prop = missing_values / float(total_values)
        if not missing_values_prop <= MAX_MISSING_PROPORTION:
            raise ce.FieldTooManyMissingsError(
                field, missing_values, positive_values
            )


# noinspection PyUnresolvedReferences
def validate_using_temporal(df, dataset_meta):
    # realiza validaciones usando el campo "temporal" de metadadta del dataset

    # sólo chequea el uso de temporal, si este existe
    if "temporal" in dataset_meta:
        try:
            ini_temporal, end_temporal = dataset_meta["temporal"].split("/")
            parse_time(ini_temporal)
            parse_time(end_temporal)
        except Exception:
            raise ce.DatasetTemporalMetadataError(dataset_meta["temporal"])
        # 4. Las series deben comenzar después del valor inicial de "temporal"
        for time_value in df.index:
            time_value = arrow.get(time_value.year, time_value.month,
                                   time_value.day)
            if not time_value >= arrow.get(ini_temporal):
                iso_time_value = time_value.isoformat()
                iso_ini_temporal = arrow.get(ini_temporal).isoformat()
                raise ce.TimeValueBeforeTemporalError(
                    iso_time_value, iso_ini_temporal)

        # 5. Las series deben terminar después de la mitad del rango "temporal"
        half_temporal = arrow.get(ini_temporal) + (
            arrow.get(end_temporal) - arrow.get(ini_temporal)
        ) / MIN_TEMPORAL_FRACTION
        end_time_value_str = "{}-{}-{}".format(
            df.index[-1].year, df.index[-1].month, df.index[-1].day)
        iso_end_index = arrow.get(end_time_value_str).isoformat()
        iso_half_temporal = half_temporal.isoformat()
        if not arrow.get(end_time_value_str) >= half_temporal:
            raise ce.TimeIndexTooShortError(
                iso_end_index, iso_half_temporal, dataset_meta["temporal"])


def validate_no_repeated_fields(catalog, distrib_meta):
    # 6. Los ids de fields no deben repetirse en todo un catálogo
    field_ids = []
    for dataset in catalog["dataset"]:
        for distribution in dataset["distribution"]:
            if ("field" in distribution and
                    distribution["identifier"] != distrib_meta["identifier"]):
                for field in distribution["field"]:
                    if field["title"] != "indice_tiempo" and "id" in field:
                        field_ids.append(field["id"])
    for field_distrib in distrib_meta["field"]:
        if "id" in field_distrib and field_distrib["id"] in field_ids:
            raise ce.FieldIdRepetitionError(field_distrib["id"])


def validate_no_repeated_titles(distrib_meta):
    # 7. Los títulos de fields no deben repetirse en una distribución
    fields = distrib_meta["field"]
    _assert_repeated_value("title", fields, ce.FieldTitleRepetitionError)


def validate_no_repeated_descriptions(distrib_meta):
    # 8. Las descripciones de fields no deben repetirse en una distribución
    fields = [field for field in distrib_meta["field"]
              if "description" in field]
    _assert_repeated_value("description", fields,
                           ce.FieldDescriptionRepetitionError)


def validate_values_are_numeric(df, distrib_meta):
    """Las series documentadas deben contener sólo valores numéricos."""
    fields_title = [
        field["title"] for field in distrib_meta["field"]
        if "specialType" not in field or field["specialType"] != "time_index"
    ]
    for field_title in fields_title:
        if not is_numeric_dtype(df[field_title]):
            raise ce.InvalidNumericField(field_title, df[field_title])


def validate_missing_fields(df, distrib_meta):
    fields = [
        field["title"] for field in distrib_meta["field"]
        if "specialType" not in field or field["specialType"] != "time_index"
    ]
    for field in fields:
        if field not in df:
            raise ce.FieldMissingInDistrbutionError(field,
                                                    distrib_meta['identifier'])


def validate_df_shape(df, distrib_meta):
    periodicity = None
    for field in distrib_meta['field']:
        if field.get('specialType') == 'time_index':
            periodicity = field.get('specialTypeDetail')

    freq = freq_iso_to_pandas(periodicity)
    new_index = pd.date_range(df.index[0], df.index[-1], freq=freq)
    columns = df.columns
    data = np.array(df)
    try:
        pd.DataFrame(index=new_index, data=data, columns=columns)

    except ValueError:
        if freq == 'D':
            freq = 'B'
            new_index = pd.date_range(df.index[0], df.index[-1], freq=freq)
            try:
                pd.DataFrame(index=new_index, data=data, columns=columns)
                return

            except ValueError:
                pass

        raise ce.DistributionBadDataError(
            distrib_meta['identifier'],
            df.index[0], df.index[-1], periodicity,
            len(new_index), len(data)
        )


def validate_header_cell_field_id(xl, worksheet, headers_coord, headers_value):
    # Las celdas de los headers deben estar en blanco o contener un id
    for header_coord, header_value in zip(headers_coord, headers_value):
        ws_header_value = xl.wb[worksheet][header_coord].value
        if ws_header_value != header_value:
            raise ce.HeaderIdError(
                worksheet, header_coord, header_value, ws_header_value)


def validate_header_cell_field_id_or_blank(
        xl, worksheet, headers_coord, headers_value):
    # Las celdas de los headers deben estar en blanco o contener un id
    for header_coord, header_value in zip(headers_coord, headers_value):
        ws_header_value = xl.wb[worksheet][header_coord].value
        if (
            ws_header_value and
            len(text_type(ws_header_value).strip()) > 0 and
            ws_header_value != header_value
        ):
            raise ce.HeaderNotBlankOrIdError(
                worksheet, header_coord, header_value, ws_header_value)


def validate_no_repeated_fields_in_distribution(distrib_meta):
    """Verifica que los ID de los fields no estén repetidos dentro de
    la misma distribución
    """
    fields = set()
    for field in distrib_meta.get('field'):
        _id = field.get('id')
        if not _id:
            continue

        if field.get('id') in fields:
            raise ce.FieldIdRepetitionError(repeated_fields=_id)

        fields.add(_id)


def validate_distinct_scraping_start_cells(distrib_meta):
    for field in distrib_meta.get("field"):
        if field.get("scrapingIdentifierCell") == field.get("scrapingDataStartCell"):
            raise ce.ScrapingStartCellsIdenticalError(
                field.get("scrapingIdentifierCell"),
                field.get("scrapingDataStartCell")
            )


def validate_distribution(df, catalog, dataset_meta, distrib_meta,
                          _=None):

    # validaciones sólo de metadatos
    validate_field_id(distrib_meta)
    validate_no_repeated_fields(catalog, distrib_meta)
    validate_no_repeated_titles(distrib_meta)
    validate_no_repeated_descriptions(distrib_meta)
    validate_no_repeated_fields_in_distribution(distrib_meta)

    # validaciones de headers
    validate_field_title(df)
    validate_title_length(df)

    # validaciones de índice de tiempo
    validate_using_temporal(df, dataset_meta)

    # validaciones de los valores de las series
    validate_missing_fields(df, distrib_meta)
    validate_values_are_numeric(df, distrib_meta)
    validate_field_few_values(df)
    validate_missing_values(df)
    validate_df_shape(df, distrib_meta)


def validate_distribution_scraping(
        xl, worksheet, headers_coord, headers_value, distrib_meta,
        force_ids=True):

    if force_ids:
        validate_header_cell_field_id(
            xl, worksheet, headers_coord, headers_value)
    else:
        validate_header_cell_field_id_or_blank(
            xl, worksheet, headers_coord, headers_value)

    validate_distinct_scraping_start_cells(distrib_meta)
