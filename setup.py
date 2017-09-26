import os
from setuptools import setup


with open(os.path.abspath("requirements.txt")) as f:
    requirements = [req.strip() for req in f.readlines()]

setup(
    name='pydatajson_ts',
    version='dev',
    packages=[
        'pydatajson_ts'
    ],
    package_dir={'pydatajson_ts': 'pydatajson_ts'},
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,

)
