import pandas as pd

from series_tiempo_ar.helpers import freq_iso_to_pandas, fix_time_index


def generate_ts_distribution_from_text_file(
    catalog, identifier, catalog_id=None, file_source=None
):
    distribution = catalog.get_distribution(identifier)
    frequency = catalog.get_distribution_time_index_frequency(distribution)
    catalog_id = catalog_id or catalog.get("identifier")

    # parámetros de lectura del archivo de texto
    sep = distribution["scrapingFileSeparator"]
    encoding = distribution["scrapingFileEncoding"]
    path = file_source or distribution["scrapingFileURL"]
    time_format = distribution["scrapingFileTimeFormat"]
    fields = _get_fields(
        distribution["scrapingFileTimeField"],
        distribution["scrapingFileIdsField"],
        distribution["scrapingFileValuesField"],
    )

    # lectura del archivo de texto según los parámetros del catálogo
    df_panel = pd.read_csv(
        path,
        sep=sep,
        names=fields["default_names"] if fields["ordinal"] else None,
        encoding=encoding,
        converters={fields["series_id_field"]: str},
    )

    # transforma los ids de las series del catálogo, eliminando el catalog_id
    # prependeado para volverlos únicos dentro de la base completa, ahora los
    # ids de las series son los mismos que el archivo original del publicador
    series = {
        ts["id"].replace(catalog_id + "_", ""): ts["title"]
        for ts in catalog.get_time_series(distribution_identifier=identifier)
    }

    # transforma dataframe de panel simple en distribución de series de tiempo
    df_series = get_series_df_from_panel(
        df_panel,
        series,
        frequency,
        time_format=time_format,
        time_field=fields["time_field"],
        series_id_field=fields["series_id_field"],
        values_field=fields["values_field"],
    )

    return df_series


def _get_fields(time_field, series_id_field, values_field):
    fields = {}

    try:
        time_field = int(time_field)
        series_id_field = int(series_id_field)
        values_field = int(values_field)

        fields["ordinal"] = True
        default_names = {
            "indice_tiempo": time_field,
            "serie_id": series_id_field,
            "valor": values_field,
        }
        sorted_default_names = sorted(
            list(default_names.items()), key=lambda tup: tup[1]
        )

        fields["default_names"] = [tup[0] for tup in sorted_default_names]
        fields["time_field"] = "indice_tiempo"
        fields["series_id_field"] = "serie_id"
        fields["values_field"] = "valor"

    except:
        fields["ordinal"] = False
        fields["default_names"] = ["serie_id", "indice_tiempo", "valor"]
        fields["time_field"] = time_field
        fields["series_id_field"] = series_id_field
        fields["values_field"] = values_field

    return fields


def get_series_df_from_panel(
    df_panel,
    series,
    time_index_freq,
    time_format="%Y-%m-%d",
    time_field="indice_tiempo",
    series_id_field="serie_id",
    values_field="valor",
):
    """Convierte tabla con id, fecha y valor en distribución de TS.

    Args:
        df_panel (pd.DataFrame): Tabla con columnas de id de series, fecha
            y valor de observaciones.
        series (dict): Donde los keys son "field_id" de series y los values
            son "field_title" de las series.
        time_field (str): Campo que tiene la fecha.
        time_format (str): Formato en el que hay que parsear la fecha.
        series_id_field (str): Campo que tiene el id de la serie.
        values_field (str): Campo que tiene los valores de las observaciones.

    return: pd.DataFrame
    """

    # parsea el campo de fechas al tipo datetime
    df_panel[time_field] = pd.to_datetime(df_panel[time_field], format=time_format)

    # se queda solo con las series elegidas
    df = df_panel[df_panel[series_id_field].isin(series.keys())]

    # construye un período continuo para el índice de tiempo, el más largo
    period_range = pd.date_range(
        min(df.indice_tiempo),
        max(df.indice_tiempo),
        freq=freq_iso_to_pandas(time_index_freq),
    )

    # cambia ids por titulos que sean nombres de campos al pivotar
    df["serie_id"] = df.serie_id.apply(series.get)

    # convierte el panel en una tabla de series de tiempo
    data = df.pivot_table(columns="serie_id", index="indice_tiempo", values="valor")

    # convierte el indice de tiempo a comienzos de periodos
    try:
        data.index = data.index.to_period(
            freq=freq_iso_to_pandas(time_index_freq, "start")
        ).to_timestamp()
    except Exception as e:
        data.index = data.index.to_period(
            freq=freq_iso_to_pandas(time_index_freq, "end")
        ).to_timestamp()

    # completa indice de tiempo con periodos faltante para que sea continuo
    df_series = pd.DataFrame(index=period_range, data=data)

    return df_series
