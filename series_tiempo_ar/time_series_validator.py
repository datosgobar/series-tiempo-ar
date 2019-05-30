from pydatajson.validation import Validator

from series_tiempo_ar.validations import get_distribution_errors


class TimeSeriesValidator(Validator):
    def _custom_errors(self, catalog):
        yield from super(TimeSeriesValidator, self)._custom_errors(catalog)

        for distribution in catalog.get_distributions(only_time_series=True):
            yield from get_distribution_errors(catalog, distribution.get("identifier"))

    def get_catalog_errors(self, catalog):
        errors = {}
        for distribution in catalog.get_distributions(only_time_series=True):
            identifier = distribution.get("identifier")
            distribution_errors = [
                e.message for e in get_distribution_errors(catalog, identifier)
            ]
            if distribution_errors:
                errors[identifier] = distribution_errors
        return errors
