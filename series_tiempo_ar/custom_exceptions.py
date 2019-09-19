#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Excepciones personalizadas para validación y registro de errores"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement


class TimeSeriesError(ValueError):
    def __init__(self, *args):
        super(TimeSeriesError, self).__init__(*args)
        self.message = args[0]
        self.validator = "time_series_format"
        self.path = []
        self.validator_value = None
        self.instance = None


class InvalidNumericField(TimeSeriesError):
    def __init__(self, field_title, values):
        msg = "'{}' tiene valores no numericos: '{}'".format(
            field_title, " ".join(list(values))
        )
        super(InvalidNumericField, self).__init__(msg)


class FieldTitleTooLongError(TimeSeriesError):
    def __init__(self, field, field_len, max_field_len):
        msg = "'{}' tiene '{}' caracteres. Maximo: '{}'".format(
            field, field_len, max_field_len
        )
        super(FieldTitleTooLongError, self).__init__(msg)


class InvalidFieldTitleError(TimeSeriesError):
    def __init__(self, field, char=None, valid_field_chars=None, is_unnamed=None):
        if is_unnamed:
            msg = "Existe un campo sin nombre en la distribucion: '{}'"
        elif char and valid_field_chars:
            msg = "'{}' usa caracteres invalidos ('{}'). Validos: '{}'".format(
                field, char, valid_field_chars
            )
        else:
            raise NotImplementedError(
                "Debe usarse 'is_unnamed' o 'char' + 'valid_field_chars'"
            )
        super(InvalidFieldTitleError, self).__init__(msg)


class InvalidFieldIdError(TimeSeriesError):
    def __init__(self, field_id, char, valid_field_chars):
        msg = "'{}' usa caracteres invalidos ('{}'). Validos: '{}'".format(
            field_id, char, valid_field_chars
        )
        super(InvalidFieldIdError, self).__init__(msg)


class TimeIndexFutureTimeValueError(TimeSeriesError):
    def __init__(self, iso_time_value, iso_now):
        msg = "{} es fecha futura respecto de {}".format(iso_time_value, iso_now)
        super(TimeIndexFutureTimeValueError, self).__init__(msg)


class FieldFewValuesError(TimeSeriesError):
    def __init__(self, field, positive_values, minimum_values):
        msg = "{} tiene {} valores, deberia tener {} o mas".format(
            field, positive_values, minimum_values
        )
        super(FieldFewValuesError, self).__init__(msg)


class FieldTooManyMissingsError(TimeSeriesError):
    def __init__(self, field, missing_values, positive_values):
        msg = "{} tiene mas missings ({}) que valores ({})".format(
            field, missing_values, positive_values
        )
        super(FieldTooManyMissingsError, self).__init__(msg)


class DatasetTemporalMetadataError(TimeSeriesError):
    def __init__(self, temporal):
        msg = "{} no es un formato de 'temporal' valido".format(temporal)
        super(DatasetTemporalMetadataError, self).__init__(msg)


class TimeValueBeforeTemporalError(TimeSeriesError):
    def __init__(self, iso_time_value, iso_ini_temporal):
        msg = "Serie comienza ({}) antes de 'temporal' ({}) ".format(
            iso_time_value, iso_ini_temporal
        )
        super(TimeValueBeforeTemporalError, self).__init__(msg)


class TimeIndexTooShortError(TimeSeriesError):
    def __init__(self, iso_end_index, iso_half_temporal, temporal):
        msg = "Serie termina ({}) antes de mitad de 'temporal' ({}) {}".format(
            iso_end_index, iso_half_temporal, temporal
        )
        super(TimeIndexTooShortError, self).__init__(msg)


class BaseRepetitionError(TimeSeriesError):

    """El id de una entidad está repetido en el catálogo."""

    def get_msg(self, entity_name, entity_type, repeated_entities, entity_id=None):
        if entity_id is not None:
            return "Hay mas de 1 {} con {} {}: {}".format(
                entity_name, entity_type, entity_id, repeated_entities
            )
        return "Hay {} con {} repetido: {}".format(
            entity_name, entity_type, repeated_entities
        )


class FieldIdRepetitionError(BaseRepetitionError):
    def __init__(self, repeated_fields, field_id=None):
        msg = self.get_msg("field", "id", repeated_fields, field_id)
        super(FieldIdRepetitionError, self).__init__(msg)


class FieldTitleRepetitionError(BaseRepetitionError):

    """Hay un campo repetido en la distribución."""

    def __init__(self, repeated_fields, field_title=None):
        msg = self.get_msg("field", "title", repeated_fields, field_title)
        super(FieldTitleRepetitionError, self).__init__(msg)


class FieldDescriptionRepetitionError(BaseRepetitionError):

    """Hay un campo repetido en la distribución."""

    def __init__(self, repeated_fields, field_desc=None):
        msg = self.get_msg("field", "description", repeated_fields, field_desc)
        super(FieldDescriptionRepetitionError, self).__init__(msg)


class DistributionIdRepetitionError(BaseRepetitionError):
    def __init__(self, repeated_distributions, distribution_id=None):
        msg = self.get_msg(
            "distribution", "id", repeated_distributions, distribution_id
        )
        super(DistributionIdRepetitionError, self).__init__(msg)


class DatasetIdRepetitionError(BaseRepetitionError):
    def __init__(self, repeated_datasets, dataset_id=None):
        msg = self.get_msg("dataset", "id", repeated_datasets, dataset_id)
        super(DatasetIdRepetitionError, self).__init__(msg)


class BaseNonExistentError(TimeSeriesError):
    @staticmethod
    def get_msg(entity_name, entity_type, entity_id):
        """El id de una entidad no existe en el catálogo."""
        return "No hay ningun {} con {} {}".format(entity_name, entity_type, entity_id)


class FieldIdNonExistentError(BaseNonExistentError):
    def __init__(self, field_id):
        msg = self.get_msg("field", "id", field_id)
        super(FieldIdNonExistentError, self).__init__(msg)


class FieldTitleNonExistentError(BaseNonExistentError):
    def __init__(self, field_title):
        msg = self.get_msg("field", "title", field_title)
        super(FieldTitleNonExistentError, self).__init__(msg)


class DistributionIdNonExistentError(BaseNonExistentError):
    def __init__(self, distribution_id):
        msg = self.get_msg("distribution", "id", distribution_id)
        super(DistributionIdNonExistentError, self).__init__(msg)


class DatasetIdNonExistentError(BaseNonExistentError):
    def __init__(self, dataset_id):
        msg = self.get_msg("dataset", "id", dataset_id)
        super(DatasetIdNonExistentError, self).__init__(msg)


class FieldMissingInDistrbutionError(TimeSeriesError):
    def __init__(self, field, distribution):
        msg = "Campo {} faltante en la distribución {}".format(field, distribution)
        super(FieldMissingInDistrbutionError, self).__init__(msg)


class DistributionBadDataError(TimeSeriesError):
    def __init__(
        self,
        distribution_id,
        time_index_ini,
        time_index_end,
        timie_index_freq,
        time_index_size,
        values_size,
    ):
        msg = (
            "Datos inconsistentes en la distribución {}: "
            "Comienzo '{}' / Fin '{}' / Frecuencia '{}' / Fechas '{}' / Valores '{}'"
        )
        msg = msg.format(
            distribution_id,
            time_index_ini,
            time_index_end,
            timie_index_freq,
            time_index_size,
            values_size,
        )
        super(DistributionBadDataError, self).__init__(msg)


class HeaderNotBlankOrIdError(TimeSeriesError):
    def __init__(self, worksheet, header_coord, header_value, ws_header_value):
        msg = "'{}' en hoja '{}' tiene '{}'. Debe ser vacio o '{}'".format(
            header_coord, worksheet, ws_header_value, header_value
        )
        super(HeaderNotBlankOrIdError, self).__init__(msg)


class HeaderIdError(TimeSeriesError):
    def __init__(self, worksheet, header_coord, header_value, ws_header_value):
        msg = "'{}' en hoja '{}' tiene '{}'. Debe ser '{}'".format(
            header_coord, worksheet, ws_header_value, header_value
        )
        super(HeaderIdError, self).__init__(msg)


class ScrapingStartCellsIdenticalError(TimeSeriesError):
    def __init__(self, scrapingIdentifierCell, scrapingDataStartCell):
        msg = "scrapingIdentifierCell ({}) es igual a scrapingDataStartCell ({})".format(
            scrapingIdentifierCell, scrapingDataStartCell
        )
        super(ScrapingStartCellsIdenticalError, self).__init__(msg)


class DistributionTooManyNullSeriesError(TimeSeriesError):
    def __init__(self, distribution, max_allowed_proportion, null_proportion):
        msg = "Proporción de series nulas en distribución {} por encima del umbral permitido ({}): {}".format(
            distribution, max_allowed_proportion, null_proportion
        )
        super(DistributionTooManyNullSeriesError, self).__init__(msg)


class NonExistentDescriptionError(TimeSeriesError):
    def __init__(self, distribution_id):
        msg = "Existen fields sin descripción en la distribución {}".format(
            distribution_id
        )
        super(NonExistentDescriptionError, self).__init__(msg)
