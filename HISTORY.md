Versiones
===

0.3.0 (2019-06-25)
------------------

* Primer release estable de la librería. Agrega métodos adicionales de validaciones, y centraliza la lectura de distribuciones en el método `TimeSeriesDataJson.load_ts_distribution`

0.2.3 (2019-03-01)
------------------

* Actualizado de validaciones para distribuciones CSV

0.1.4 (2018-05-06)
------------------

* Flexibiliza la restricción de series demasiado cortas: ahora se admite hasta un 2% del total de las series de una distribución con una cantidad demasiado baja de valores para ser una serie.

0.1.3 (2018-05-04)
------------------

* Actualiza las validaciones al schema de la versión 0.4.12 de pydatajson

0.1.2 (2018-04-30)
------------------

* El campo `temporal` en dataset pasa a ser de uso opcional.

0.1.0 (2018-04-17)
------------------

* Soporte para Python 3

0.0.3 (2017-10-18)
------------------

* Restauro la validación `validate_df_shape` que está testeada y corregida.
* Flexibilizo al límite el máximo de missings admitidos en una serie (999 missings por cada 1000 valores).

0.0.2 (2017-10-10)
------------------

* Bug fix: elimino temporalmente validación `validate_df_shape` que tiene algún error en el tratamiento de los tipos.

0.0.1 (2017-10-08)
------------------

* Primer release a PyPI.
* Release todavía no documentado.
