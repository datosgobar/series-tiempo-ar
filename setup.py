#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

with open("requirements.txt") as f:
    requirements = [req.strip() for req in f.readlines()]

with open("requirements_dev.txt") as f:
    test_requirements = [req.strip() for req in f.readlines()]

setup(
    name='series-tiempo-ar',
    version='0.1.2',
    description="Módulos para extraer, analizar y compilar series de tiempo documentadas en catálogos de datos abiertos basados en el perfil de metadatos del Paquete de Apertura de Datos.",
    long_description=readme + '\n\n' + history,
    author="Datos Argentina",
    author_email='datos@modernizacion.gob.ar',
    url='https://github.com/datosgobar/series-tiempo-ar',
    packages=[
        'series_tiempo_ar',
    ],
    package_dir={'series_tiempo_ar':
                 'series_tiempo_ar'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='series_tiempo_ar',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
