#! coding: utf-8
import logging
import chardet
import csv
import arrow
from copy import deepcopy
import pandas as pd


def parse_time_value(value, frequency):
    """Lee una fecha según su frecuencia."""

    if frequency == "A":
        return arrow.get(value).replace(day=1).replace(month=1)
    elif (frequency == "6M" or frequency == "Q" or frequency == "M"):
        return arrow.get(value).replace(day=1)
    else:
        return arrow.get(value)


def increment_period(value, periods, frequency):
    """Incrementa una fecha en X períodos, según su frecuencia."""

    if frequency == "A":
        return value.replace(years=+periods)
    elif frequency == "6M":
        return value.replace(months=+(6 * periods))
    elif frequency == "Q":
        return value.replace(months=+(3 * periods))
    elif frequency == "M":
        return value.replace(months=+periods)
    elif frequency == "D":
        return value.replace(days=+periods)
    else:
        raise Exception("No se reconoce la frecuencia {}".format(frequency))


def fix_time_index(time_values, values, frequency):
    """Toma lista de fechas y valores, para arreglar índice según frec."""

    new_time_values = []
    new_values = []

    previous_time_value = None
    previous_value = None

    current_time_value = None
    current_value = None

    for next_time_value, next_value in zip(list(time_values), list(values)):
        next_time_value = parse_time_value(next_time_value, frequency)

        # cuando empieza a iterar, todavía no tiene valores anteriores
        if not current_time_value:
            current_time_value = deepcopy(next_time_value)
            current_value = deepcopy(next_value)

            new_time_values.append(deepcopy(current_time_value))
            new_values.append(deepcopy(current_value))

        # cuando empieza a iterar, todavía no tiene valores anteriores
        elif not previous_time_value:
            previous_time_value = deepcopy(current_time_value)
            previous_value = deepcopy(current_value)
            current_time_value = deepcopy(next_time_value)
            current_value = deepcopy(next_value)

        # cuando tiene valores anteriores, comienza a buscar errores
        # corregibles
        else:
            expected_current = increment_period(
                previous_time_value, 1, frequency)
            expected_next = increment_period(previous_time_value, 2, frequency)

            # arregla período incorrecto, si anterior y siguiente son correctos
            if (
                (current_time_value != expected_current) and
                (next_time_value == expected_next)
            ):
                current_time_value = deepcopy(expected_current)

            elif (
                (current_time_value > expected_current) and
                (next_time_value > expected_next)
            ):
                # agrega todos los missings faltantes en el índice
                while current_time_value > expected_current:
                    new_time_values.append(deepcopy(expected_current))
                    new_values.append(pd.np.nan)

                    previous_time_value = increment_period(
                        previous_time_value, 1, frequency)
                    previous_value = pd.np.nan

                    expected_current = increment_period(
                        expected_current, 1, frequency)
                    expected_next = increment_period(
                        expected_next, 1, frequency)

            # agrega a la lista el nuevo valor, una vez corregido
            new_time_values.append(deepcopy(current_time_value))
            new_values.append(deepcopy(current_value))

            # incrementa los valores anteriores, para la próxima iteración
            previous_time_value = deepcopy(current_time_value)
            previous_value = deepcopy(current_value)
            current_time_value = deepcopy(next_time_value)
            current_value = deepcopy(next_value)

    # agrega el último valor, después de las iteraciones
    new_time_values.append(deepcopy(next_time_value))
    new_values.append(deepcopy(next_value))

    new_time_values_str = [
        value.format("YYYY-MM-DD") for value in new_time_values]

    return new_time_values_str, new_values


def freq_iso_to_pandas(freq_iso8601, how="start"):
    frequencies_map_start = {
        "R/P1Y": "AS",
        "R/P6M": "6MS",
        "R/P3M": "QS",
        "R/P1M": "MS",
        "R/P1D": "D"
    }
    frequencies_map_end = {
        "R/P1Y": "A",
        "R/P6M": "6M",
        "R/P3M": "Q",
        "R/P1M": "M",
        "R/P1D": "D"
    }
    if how == "start":
        return frequencies_map_start[freq_iso8601]
    elif how == "end":
        return frequencies_map_end[freq_iso8601]
    else:
        raise Exception(
            "{} no se reconoce para 'how': debe ser 'start' o 'end'".format(
                how))


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logging_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(logging_formatter)
    # logger.addHandler(ch)

    return logger


def find_encoding(f_path):
    """Identifica el encoding en un archivo CSV.

    Args:
        f_path (str): Path al archivo

    Returns:
        str: Encoding o mensaje 'no identificado'
    """
    r_file = open(f_path, 'rb').read()
    try:
        encoding = chardet.detect(r_file)['encoding']
        print("Encoding estimado automáticamente: {}".format(encoding))
        return encoding
    except Exception:
        print("Encoding no pudo ser estimado automáticamente")
        return None


def find_dialect(f_path):
    """Identifica el dialecto de un archivo CSV (caracter delimitador de campos
     y de texto).

    Args:
        f_path (str): Path al archivo

    Returns:
        tuple: Caracter delimitador de campos y caracter delimitador de texto,
    """
    with open(f_path, 'rb') as csvfile:
        line = csvfile.readline().decode('utf-8', errors='ignore')
        dialect = csv.Sniffer().sniff(line)
        print('Detección automática separador ("{}") y comillas ("{}")'.format(
            dialect.delimiter, dialect.quotechar))
        return dialect.delimiter, dialect.quotechar
