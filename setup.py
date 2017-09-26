import os
from setuptools import setup


with open(os.path.abspath("requirements.txt")) as f:
    requirements = [req.strip() for req in f.readlines()]

setup(
    name='pydatajson-ts',
    version='0.0.1',
    packages=['pydatajson_ts'],
    package_dir={'pydatajson_ts':'pydatajson_ts'},
    zip_safe=False,
    install_requires=requirements,
)
