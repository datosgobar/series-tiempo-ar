#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Módulo principal de series-tiempo-ar

Contiene una extensión del objeto DataJson para catálogos con series de tiempo.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import os
import pandas as pd

from pydatajson import DataJson

from helpers import get_logger


class TimeSeriesDataJson(DataJson):
    """Métodos para trabajar con catálogos de series de tiempo en data.json."""

    pass
