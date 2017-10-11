#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests del modulo series_tiempo_ar."""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement

import os
import unittest
import nose

import pandas as pd
from pydatajson import DataJson
from series_tiempo_ar.validations import validate_distribution


class SeriesTiempoArTestCase(unittest.TestCase):

    SAMPLES_DIR = os.path.join("tests", "samples")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_validate(self):
        catalog = os.path.join(self.SAMPLES_DIR, 'data.json')
        catalog = DataJson(catalog)
        distrib_meta = catalog.get_distribution(identifier="125.1")
        df = pd.read_csv(distrib_meta['downloadURL'],
                         parse_dates=['indice_tiempo']
                         ).set_index('indice_tiempo')
        dataset_meta = catalog.get_dataset(
            identifier=distrib_meta['dataset_identifier']
        )

        validate_distribution(df, catalog, dataset_meta, distrib_meta)

    def test_validate_business_date(self):
        catalog = os.path.join(self.SAMPLES_DIR, 'data_business_days.json')
        catalog = DataJson(catalog)
        identifier = "133.1"
        distribution = catalog.get_distribution(identifier=identifier)
        dataset = catalog.get_dataset(
            identifier=distribution['dataset_identifier'])

        df = pd.read_csv(distribution['downloadURL'],
                         parse_dates=['indice_tiempo']) \
            .set_index('indice_tiempo')

        validate_distribution(df, catalog, dataset, distribution)


if __name__ == '__main__':
    nose.run(defaultTest=__name__)
