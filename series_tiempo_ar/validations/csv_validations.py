import string

import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype

from series_tiempo_ar import custom_exceptions as ce
from series_tiempo_ar.helpers import freq_iso_to_pandas

MINIMUM_VALUES = 2
MAX_MISSING_PROPORTION = 0.999
MAX_TOO_SMALL_PROPORTION = 0.02
MIN_TEMPORAL_FRACTION = 10
MAX_FIELD_TITLE_LEN = 60
MAX_NULL_SERIES_PROPORTION = 0.20


def _assert_repeated_value(field_name, field_values, exception):
    fields = pd.Series([field[field_name] for field in field_values])
    field_dups = fields[fields.duplicated()].values
    if field_dups.size > 0:
        raise exception(repeated_fields=field_dups)


def validate_field_few_values(df, _distrib_meta, _catalog):
    # La mayoría de las series de una distrib. deben tener un mínimo de valores
    series_too_small = 0
    series_total = len(df.columns)

    for field in df.columns:
        not_null_values = len(df[field][df[field].notnull()])

        # se suma una nueva serie demasiado corta (si está vacía no la cuento)
        if not_null_values > 0 and not not_null_values >= MINIMUM_VALUES:
            series_too_small += 1

        # chequea si hay demasiadas series cortas
        if float(series_too_small) / series_total > MAX_TOO_SMALL_PROPORTION:
            raise ce.FieldFewValuesError(field, not_null_values, MINIMUM_VALUES)


def validate_distribution_null_series_amount(df, distrib_meta, _catalog):
    distribution_identifier = distrib_meta["identifier"]
    series_total = len(df.columns)
    null_series_amount = 0

    for field in df.columns:
        not_null_values = len(df[field][df[field].notnull()])
        if not_null_values == 0:
            null_series_amount += 1

    null_proportion = float(null_series_amount) / series_total
    if null_proportion >= MAX_NULL_SERIES_PROPORTION:
        raise ce.DistributionTooManyNullSeriesError(
            distribution_identifier, MAX_NULL_SERIES_PROPORTION, null_proportion
        )


def validate_field_title(df, _distrib_meta, _catalog):
    # Los titulos de los campos deben tener caracteres ASCII + "_"
    valid_field_chars = "abcdefghijklmnopqrstuvwxyz0123456789_"
    for field in df.columns:
        if "unnamed" in field.lower():
            raise ce.InvalidFieldTitleError(field, is_unnamed=True)
        for char in field:
            if char not in valid_field_chars:
                raise ce.InvalidFieldTitleError(
                    field, char=char, valid_field_chars=valid_field_chars
                )


def validate_field_id(_df, distrib_meta, _catalog):
    # Los ids de los campos deben tener caracteres ASCII + "_"
    special_chars = "_-."
    valid_field_chars = string.ascii_letters + string.digits + special_chars
    for field_id in [field["id"] for field in distrib_meta["field"] if "id" in field]:
        for char in field_id:
            if char not in valid_field_chars:
                raise ce.InvalidFieldIdError(field_id, char, valid_field_chars)


def validate_title_length(df, _distrib_meta, _catalog):
    # Los nombres de los campos tienen que tener un máximo de caracteres
    for field in df.columns:
        if len(field) > MAX_FIELD_TITLE_LEN:
            raise ce.FieldTitleTooLongError(field, len(field), MAX_FIELD_TITLE_LEN)


def validate_missing_values(df, _distrib_meta, _catalog):
    # Las series deben tener una proporción máxima de missings
    for field in df.columns:
        total_values = len(df[field])
        positive_values = len(df[field][df[field].notnull()])
        missing_values = total_values - positive_values
        missing_values_prop = missing_values / float(total_values)
        if not missing_values_prop <= MAX_MISSING_PROPORTION:
            raise ce.FieldTooManyMissingsError(field, missing_values, positive_values)


def validate_no_repeated_fields(_df, distrib_meta, catalog):
    # 6. Los ids de fields no deben repetirse en todo un catálogo
    field_ids = []
    for dataset in catalog["dataset"]:
        for distribution in dataset["distribution"]:
            if (
                "field" in distribution
                and distribution["identifier"] != distrib_meta["identifier"]
            ):
                for field in distribution["field"]:
                    if field["title"] != "indice_tiempo" and "id" in field:
                        field_ids.append(field["id"])
    for field_distrib in distrib_meta["field"]:
        if "id" in field_distrib and field_distrib["id"] in field_ids:
            raise ce.FieldIdRepetitionError(field_distrib["id"])


def validate_no_repeated_titles(_df, distrib_meta, _catalog):
    # 7. Los títulos de fields no deben repetirse en una distribución
    fields = distrib_meta["field"]
    _assert_repeated_value("title", fields, ce.FieldTitleRepetitionError)


def validate_no_repeated_descriptions(_df, distrib_meta, _catalog):
    # 8. Las descripciones de fields no deben repetirse en una distribución
    fields = [field for field in distrib_meta["field"] if "description" in field]
    _assert_repeated_value("description", fields, ce.FieldDescriptionRepetitionError)


def validate_values_are_numeric(df, distrib_meta, _catalog):
    """Las series documentadas deben contener sólo valores numéricos."""
    fields_title = [
        field["title"]
        for field in distrib_meta["field"]
        if (field.get("specialType", "time_index") != "time_index")
        and field.get("title") in list(df.columns)
    ]
    for field_title in fields_title:
        if not is_numeric_dtype(df[field_title]):
            raise ce.InvalidNumericField(field_title, df[field_title])


def validate_missing_fields(df, distrib_meta, _catalog):
    fields = [
        field["title"]
        for field in distrib_meta["field"]
        if "specialType" not in field or field["specialType"] != "time_index"
    ]
    for field in fields:
        if field not in df:
            raise ce.FieldMissingInDistrbutionError(field, distrib_meta["identifier"])


def validate_df_shape(df, distrib_meta, _catalog):
    periodicity = None
    for field in distrib_meta["field"]:
        if field.get("specialType") == "time_index":
            periodicity = field.get("specialTypeDetail")

    freq = freq_iso_to_pandas(periodicity)
    new_index = pd.date_range(df.index[0], df.index[-1], freq=freq)
    columns = df.columns
    data = np.array(df)
    try:
        pd.DataFrame(index=new_index, data=data, columns=columns)

    except ValueError:
        if freq == "D":
            freq = "B"
            new_index = pd.date_range(df.index[0], df.index[-1], freq=freq)
            try:
                pd.DataFrame(index=new_index, data=data, columns=columns)
                return

            except ValueError:
                pass

        raise ce.DistributionBadDataError(
            distrib_meta["identifier"],
            df.index[0],
            df.index[-1],
            periodicity,
            len(new_index),
            len(data),
        )


def validate_no_repeated_fields_in_distribution(_df, distrib_meta, _catalog):
    """Verifica que los ID de los fields no estén repetidos dentro de
    la misma distribución
    """
    fields = set()
    for field in distrib_meta.get("field"):
        _id = field.get("id")
        if not _id:
            continue

        if field.get("id") in fields:
            raise ce.FieldIdRepetitionError(repeated_fields=_id)

        fields.add(_id)


def validate_field_descriptions(_df, distrib_meta, _catalog):
    fields = [
        x
        for x in distrib_meta.get("field", [])
        if not x.get("specialType") == "time_index"
    ]
    for field in fields:
        if "description" not in field:
            raise ce.NonExistentDescriptionError(distrib_meta["identifier"])
