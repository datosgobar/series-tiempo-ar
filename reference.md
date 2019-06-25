# API Reference

## `TimeSeriesDataJson`

La clase extiende `DataJson` de [pydatajson](https://github.com/datosgobar/pydatajson). Ver su documentación para ver las funcionalidades de la clase base.

### Validaciones

`validate_time_series_catalog(self)`

Ejecuta todas las validaciones sobre las distribuciones de series de tiempo del catálogo, devolviendo una estructura de datos con los errores encontrados, con los `identifier` de distribuciones como clave, y listas de errores encontrados como valor. Si una distribución no contiene errores, no aparecerá en el diccionario.

```
{
  '123.1': [
    Error1,
    Error2
  ],
  '123.2': [
    Error1,
    Error2,
  ],
  ...
}
```

### Lectura de distribuciones de series de tiempo

```load_ts_distribution(
        self,
        identifier,
        catalog_id=None,
        is_text_file=None,
        is_excel_file=None,
        is_csv_file=None,
        file_source=None,
```

Carga una distribución de series de tiempo como un DataFrame de [pandas](https://pandas.pydata.org/pandas-docs/stable/). Obligatoriamente se debe especificar el `identifier` de la distribución dentro del catálogo a levantar. La librería inferirá el formato del archivo, pero opcionalmente se puede forzar un método de lectura con los parámetros `is_text_file`, `is_csv_file`, `is_excel_file`. 

`catalog_id` representa el ID del catálogo dentro del archivo de scraping si el archivo de la distribución a cargar es de tipo `text`.

Alternativamente se puede especificar un `file_source` para leer el archivo de un archivo de fuente local en vez de la URL de descarga en el catálogo.


## Validador

En el módulo `validations.validator` se encuentran validadores de distribuciones:


`validate_distribution(df, catalog, _dataset_meta, distrib_meta)`

Valida una distribución individual. Lanza una excepción ante el primer error encontrado. La excepción será una subclase de `TimeSeriesError`. Se mantiene por razones _legacy_, pero se recomienda utilizar `get_distribution_errors` que cuenta con una API simplificada.


`get_distribution_errors(catalog, distribution_id)`

Obtiene todos los errores de la distribución con id `distribution_id` dentro del catálogo de series de tiempo (`TimeSeriesDataJson`) `catalog`. Devuelve una lista de errores encontrados, que son subclases de `TimeSeriesError`.

```
def validate_distribution_scraping(
    xl, worksheet, headers_coord, headers_value, distrib_meta, force_ids=True
)
```

Valida una _worksheet_ de scraping de xlsx. Lanza excepciones subclase de `TimeSeriesError` si falla alguna validación.

