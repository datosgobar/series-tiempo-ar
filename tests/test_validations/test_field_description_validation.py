from unittest import TestCase

from series_tiempo_ar.custom_exceptions import NonExistentDescriptionError
from series_tiempo_ar.validations.csv_validations import FieldDescriptionsValidation
from tests.helpers import read_data_json


class ValidateDescriptionExistsTests(TestCase):
    def test_distribution_with_no_field_description_raises_error(self):
        catalog = read_data_json("missing_field_description.json")
        distribution = catalog.get_distributions()[0]
        df = None
        with self.assertRaises(NonExistentDescriptionError):
            FieldDescriptionsValidation(df, distribution, catalog).validate()
