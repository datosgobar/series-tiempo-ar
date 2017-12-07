
# Series de Tiempo de la República Argentina

[![Coverage Status](https://coveralls.io/repos/github/datosgobar/series-tiempo-ar/badge.svg?branch=master)](https://coveralls.io/github/datosgobar/series-tiempo-ar?branch=master)
[![Build Status](https://travis-ci.org/datosgobar/series-tiempo-ar.svg?branch=master)](https://travis-ci.org/datosgobar/series-tiempo-ar)
[![PyPI](https://badge.fury.io/py/series-tiempo-ar.svg)](http://badge.fury.io/py/series-tiempo-ar)
[![Stories in Ready](https://badge.waffle.io/datosgobar/series-tiempo-ar.png?label=ready&title=Ready)](https://waffle.io/datosgobar/series-tiempo-ar)
[![Documentation Status](http://readthedocs.org/projects/series-tiempo-ar/badge/?version=latest)](http://series-tiempo-ar.readthedocs.org/en/latest/?badge=latest)

* Versión python: 2
* Licencia: MIT license
* Documentación: [https://series-tiempo-ar.readthedocs.io](https://series-tiempo-ar.readthedocs.io)

El proyecto Series de Tiempo se basa en una extensión del perfil de metadatos de la política de apertura. Esta fue diseñada para facilitar la publicación de series de tiempo de organismos gubernamentales que son parte de la Red de Nodos de Datos Abiertos de la República Argentina.

A partir de esta especificación, se desarrollaron aplicaciones para extraer y compilar las series en una base de datos unificada que permitiera el desarrollo de una API.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

## Indice

- [Repositorios oficiales](#repositorios-oficiales)
- [Repositorios de terceros](#repositorios-de-terceros)
- [Instalación](#instalaci%C3%B3n)
- [Uso](#uso)
- [Tests](#tests)
- [Contacto](#contacto)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Repositorios oficiales

* [`series-tiempo-ar`](https://github.com/datosgobar/series-tiempo-ar): Paquete de módulos con funcionalidades para extraer, transformar y analizar series de tiempo basados en la versión 1.1 del [`Perfil de Metadatos`](http://paquete-apertura-datos.readthedocs.io/es/stable/guia_metadatos.html) del [`Paquete de Apertura de Datos de la República Argentina`](http://paquete-apertura-datos.readthedocs.io). Es una extensión de [`pydatajson`](https://github.com/datosgobar/pydatajson) y la dependencia principal de los otros repositorios del proyecto.

* [`series-tiempo-ar-etl`](https://github.com/datosgobar/series-tiempo-ar-etl): Rutinas de ETL usadas para compilar diariamente la [`Base de Series de Tiempo de la Administración Pública Nacional`](http://datos.gob.ar/dataset/base-series-tiempo-administracion-publica-nacional).

* [`series-tiempo-ar-api`](https://github.com/datosgobar/series-tiempo-ar-api): Aplicación basada en Django que extrae series de tiempo de los catálogos de datos abiertos de la Red de Nodos y las indexa en un motor Elastic Search para su consumo como servicio web.

* [`series-tiempo-ar-landing`](https://github.com/datosgobar/series-tiempo-ar-landing): Landing web configurable para una sencilla publicación y visualización de series de tiempo.

## Repositorios de terceros

* ¡Todavía no hay ninguno! ¿No deberías ser el primero? Si escribiste una librería para usar la API o la base completa en algún lenguaje, [nos gustaría saberlo](https://github.com/datosgobar/series-tiempo-ar/issues/new?title=Nueva librería en {lenguaje} para usar la API).

## Instalación

* **Producción:** Desde cualquier parte

```bash
$ pip install series-tiempo-ar
```

* **Desarrollo:** Clonar este repositorio, y desde su raíz, ejecutar:
```bash
$ pip install -e .
```

## Uso

*Este paquete todavía está en desarrollo incipiente y su funcionalidad no está documentada ni lista para ser distribuida.*

## Tests

Los tests se corren con `nose`. Desde la raíz del repositorio:

**Configuración inicial:**

```bash
$ pip install -r requirements_dev.txt
$ mkdir tests/temp
```

**Correr la suite de tests:**

```bash
$ nosetests
```

## Contacto

Te invitamos a [crearnos un issue](https://github.com/datosgobar/series-tiempo-ar/issues/new?title=Encontre un bug en series-tiempo-ar) en caso de que encuentres algún bug o tengas feedback de alguna parte de `series-tiempo-ar`.

Para todo lo demás, podés mandarnos tu comentario o consulta a [datos@modernizacion.gob.ar](mailto:datos@modernizacion.gob.ar).
