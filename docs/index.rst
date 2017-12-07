Series de Tiempo de la República Argentina
======================================

El proyecto Series de Tiempo se basa en una extensión del perfil de metadatos de la política de apertura. Esta fue diseñada para facilitar la publicación de series de tiempo de organismos gubernamentales que son parte de la Red de Nodos de Datos Abiertos de la República Argentina.

A partir de esta especificación, se desarrollaron aplicaciones para extraer y compilar las series en una base de datos unificada que permitiera el desarrollo de una API.

**Repositorios oficiales que componen el proyecto:**

* `series-tiempo-ar <https://github.com/datosgobar/series-tiempo-ar>`_: Paquete de módulos con funcionalidades para extraer, transformar y analizar series de tiempo basados en la versión 1.1 del `Perfil de Metadatos <http://paquete-apertura-datos.readthedocs.io/es/stable/guia_metadatos.html>`_ del `Paquete de Apertura de Datos de la República Argentina <http://paquete-apertura-datos.readthedocs.io>`_. Es una extensión de `pydatajson <https://github.com/datosgobar/pydatajson>`_ y la dependencia principal de los otros repositorios del proyecto.

* `series-tiempo-ar-etl <https://github.com/datosgobar/series-tiempo-ar-etl>`_: Rutinas de ETL usadas para compilar diariamente la `Base de Series de Tiempo de la Administración Pública Nacional <http://datos.gob.ar/dataset/base-series-tiempo-administracion-publica-nacional>`_.

* `series-tiempo-ar-api <https://github.com/datosgobar/series-tiempo-ar-api>`_: Aplicación basada en Django que extrae series de tiempo de los catálogos de datos abiertos de la Red de Nodos y las indexa en un motor Elastic Search para su consumo como servicio web.

* `series-tiempo-ar-landing <https://github.com/datosgobar/series-tiempo-ar-landing>`_: Landing web configurable para una sencilla publicación y visualización de series de tiempo.

Indice
======

.. toctree::
   :maxdepth: 2

   README.md
   HISTORY.md

Referencia librería
===================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
