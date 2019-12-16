import string

import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype

from series_tiempo_ar import custom_exceptions as ce
from series_tiempo_ar.helpers import freq_iso_to_pandas

DEFAULT_OPTIONS = {
    "minimum_values": 2,
    "max_missing_proportion": 0.999,
    "max_too_small_proportion": 0.02,
    "min_temporal_fraction": 10,
    "max_field_title_len": 60,
    "max_null_series_proportion": 0.2,
}


class ValidationOptions:
    def __init__(
        self,
        minimum_values,
        max_missing_proportion,
        max_too_small_proportion,
        min_temporal_fraction,
        max_field_title_len,
        max_null_series_proportion,
    ):
        self.minimum_values = minimum_values
        self.max_missing_proportion = max_missing_proportion
        self.max_too_small_proportion = max_too_small_proportion
        self.min_temporal_fraction = min_temporal_fraction
        self.max_field_title_len = max_field_title_len
        self.max_null_series_proportion = max_null_series_proportion

    @classmethod
    def create_with_defaults(cls, **kwargs):
        options = DEFAULT_OPTIONS.copy()

        options.update(kwargs)
        return cls(**options)


def _assert_repeated_value(field_name, field_values, exception):
    fields = pd.Series([field[field_name] for field in field_values])
    field_dups = fields[fields.duplicated()].values
    if field_dups.size > 0:
        raise exception(field_dups)


class BaseValidation:
    def __init__(self, df=None, distrib_meta=None, catalog=None, options=None):
        if options is None:
            options = ValidationOptions(**DEFAULT_OPTIONS)

        self.df = df
        self.distrib_meta = distrib_meta
        self.catalog = catalog
        self.options = options

    def validate(self):
        raise NotImplementedError


class FieldViewValuesValidation(BaseValidation):
    def validate(self):
        # La mayoría de las series de una distrib. deben tener un mínimo de valores
        series_too_small = 0
        series_total = len(self.df.columns)

        for field in self.df.columns:
            not_null_values = len(self.df[field][self.df[field].notnull()])

            # se suma una nueva serie demasiado corta (si está vacía no la cuento)
            if 0 < not_null_values < self.options.minimum_values:
                series_too_small += 1

            # chequea si hay demasiadas series cortas
            if (
                float(series_too_small) / series_total
                > self.options.max_too_small_proportion
            ):
                raise ce.FieldFewValuesError(
                    field, not_null_values, self.options.minimum_values
                )


class DistributionNullSeriesValidation(BaseValidation):
    def validate(self):
        distribution_identifier = self.distrib_meta["identifier"]
        series_total = len(self.df.columns)
        null_series_amount = 0

        for field in self.df.columns:
            not_null_values = len(self.df[field][self.df[field].notnull()])
            if not_null_values == 0:
                null_series_amount += 1

        null_proportion = float(null_series_amount) / series_total
        if null_proportion >= self.options.max_null_series_proportion:
            raise ce.DistributionTooManyNullSeriesError(
                distribution_identifier,
                self.options.max_null_series_proportion,
                null_proportion,
            )


class FieldTitleValidation(BaseValidation):
    def validate(self):
        # Los titulos de los campos deben tener caracteres ASCII + "_"
        valid_field_chars = "abcdefghijklmnopqrstuvwxyz0123456789_"
        for field in self.df.columns:
            if "unnamed" in field.lower():
                raise ce.InvalidFieldTitleError(field, is_unnamed=True)
            for char in field:
                if char not in valid_field_chars:
                    raise ce.InvalidFieldTitleError(
                        field, char=char, valid_field_chars=valid_field_chars
                    )


class FieldIdValidation(BaseValidation):
    def validate(self):
        # Los ids de los campos deben tener caracteres ASCII + "_"
        special_chars = "_-."
        valid_field_chars = string.ascii_letters + string.digits + special_chars
        for field_id in [
            field["id"] for field in self.distrib_meta["field"] if "id" in field
        ]:
            for char in field_id:
                if char not in valid_field_chars:
                    raise ce.InvalidFieldIdError(field_id, char, valid_field_chars)


class TitleLengthValidation(BaseValidation):
    def validate(self):
        # Los nombres de los campos tienen que tener un máximo de caracteres
        for field in self.df.columns:
            if len(field) > self.options.max_field_title_len:
                raise ce.FieldTitleTooLongError(
                    field, len(field), self.options.max_field_title_len
                )


class MissingValuesValidation(BaseValidation):
    def validate(self):
        # Las series deben tener una proporción máxima de missings
        for field in self.df.columns:
            total_values = len(self.df[field])
            positive_values = len(self.df[field][self.df[field].notnull()])
            missing_values = total_values - positive_values
            missing_values_prop = missing_values / float(total_values)
            if not missing_values_prop <= self.options.max_missing_proportion:
                raise ce.FieldTooManyMissingsError(
                    field, missing_values, positive_values
                )


class NoRepeatedFieldsValidation(BaseValidation):
    def validate(self):
        # 6. Los ids de fields no deben repetirse en todo un catálogo
        field_ids = []
        for dataset in self.catalog["dataset"]:
            for distribution in dataset["distribution"]:
                if (
                    "field" in distribution
                    and distribution["identifier"] != self.distrib_meta["identifier"]
                ):
                    for field in distribution["field"]:
                        if field.get("title") != "indice_tiempo" and "id" in field:
                            field_ids.append(field["id"])
        for field_distrib in self.distrib_meta.get("field", []):
            if "id" in field_distrib and field_distrib["id"] in field_ids:
                raise ce.FieldIdRepetitionError(field_distrib["id"])


class NoRepeatedTitlesValidation(BaseValidation):
    def validate(self):
        # 7. Los títulos de fields no deben repetirse en una distribución
        fields = self.distrib_meta["field"]
        _assert_repeated_value("title", fields, ce.FieldTitleRepetitionError)


class NoRepeatedDescriptionsValidation(BaseValidation):
    def validate(self):
        # 8. Las descripciones de fields no deben repetirse en una distribución
        fields = [
            field for field in self.distrib_meta["field"] if "description" in field
        ]
        _assert_repeated_value(
            "description", fields, ce.FieldDescriptionRepetitionError
        )


class ValuesAreNumericValidation(BaseValidation):
    def validate(self):
        """Las series documentadas deben contener sólo valores numéricos."""
        fields_title = [
            field["title"]
            for field in self.distrib_meta["field"]
            if (field.get("specialType", "time_index") != "time_index")
            and field.get("title") in list(self.df.columns)
        ]
        for field_title in fields_title:
            if not is_numeric_dtype(self.df[field_title]):
                raise ce.InvalidNumericField(field_title, self.df[field_title])


class MissingFieldsValidation(BaseValidation):
    def validate(self):
        fields = [
            field["title"]
            for field in self.distrib_meta["field"]
            if "specialType" not in field or field["specialType"] != "time_index"
        ]
        for field in fields:
            if field not in self.df:
                raise ce.FieldMissingInDistrbutionError(
                    field, self.distrib_meta["identifier"]
                )


class DataFrameShapeValidation(BaseValidation):
    def validate(self):
        periodicity = None
        for field in self.distrib_meta["field"]:
            if field.get("specialType") == "time_index":
                periodicity = field.get("specialTypeDetail")

        freq = freq_iso_to_pandas(periodicity)
        new_index = pd.date_range(self.df.index[0], self.df.index[-1], freq=freq)
        columns = self.df.columns
        data = np.array(self.df)
        try:
            pd.DataFrame(index=new_index, data=data, columns=columns)

        except ValueError:
            if freq == "D":
                freq = "B"
                new_index = pd.date_range(
                    self.df.index[0], self.df.index[-1], freq=freq
                )
                try:
                    pd.DataFrame(index=new_index, data=data, columns=columns)
                    return

                except ValueError:
                    pass

            raise ce.DistributionBadDataError(
                self.distrib_meta["identifier"],
                self.df.index[0],
                self.df.index[-1],
                periodicity,
                len(new_index),
                len(data),
            )


class NoRepeatedFieldsInDistributionValidation(BaseValidation):
    def validate(self):
        """Verifica que los ID de los fields no estén repetidos dentro de
        la misma distribución
        """
        fields = set()
        for field in self.distrib_meta.get("field"):
            _id = field.get("id")
            if not _id:
                continue

            if field.get("id") in fields:
                raise ce.FieldIdRepetitionError(_id)

            fields.add(_id)


class FieldDescriptionsValidation(BaseValidation):
    def validate(self):
        fields = [
            x
            for x in self.distrib_meta.get("field", [])
            if not x.get("specialType") == "time_index"
        ]
        for field in fields:
            if "description" not in field:
                raise ce.NonExistentDescriptionError(self.distrib_meta["identifier"])
