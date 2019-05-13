#!/usr/bin/env bash

set -e;

nosetests
bash scripts/black.sh
bash scripts/pylint.sh --full
