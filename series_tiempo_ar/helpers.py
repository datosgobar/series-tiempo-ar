#! coding: utf-8
import logging
from copy import deepcopy

import arrow
import pandas as pd


def parse_time_value(value, frequency):
    """Lee una fecha según su frecuencia."""

    if frequency == "A":
        return arrow.get(value).replace(day=1).replace(month=1)
    if frequency in ["6M", "Q", "M"]:
        return arrow.get(value).replace(day=1)

    return arrow.get(value)


def increment_period(value, periods, frequency):
    """Incrementa una fecha en X períodos, según su frecuencia."""

    actions = {
        "A": lambda: value.replace(years=+periods),
        "6M": lambda: value.replace(months=+(6 * periods)),
        "Q": lambda: value.replace(months=+(3 * periods)),
        "M": lambda: value.replace(months=+periods),
        "D": lambda: value.replace(days=+periods),
    }
    try:
        return actions[frequency]()
    except KeyError:
        raise ValueError("No se reconoce la frecuencia {}".format(frequency))


def fix_time_index(time_values, values, frequency):
    """Toma lista de fechas y valores, para arreglar índice según frec."""

    new_time_values = []
    new_values = []

    previous_time_value = None

    current_time_value = None
    current_value = None

    next_time_value = None
    next_value = None
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
            current_time_value = deepcopy(next_time_value)
            current_value = deepcopy(next_value)

        # cuando tiene valores anteriores, comienza a buscar errores
        # corregibles
        else:
            expected_current = increment_period(previous_time_value, 1, frequency)
            expected_next = increment_period(previous_time_value, 2, frequency)

            # arregla período incorrecto, si anterior y siguiente son correctos
            if (current_time_value != expected_current) and (
                next_time_value == expected_next
            ):
                current_time_value = deepcopy(expected_current)

            elif (current_time_value > expected_current) and (
                next_time_value > expected_next
            ):
                # agrega todos los missings faltantes en el índice
                while current_time_value > expected_current:
                    new_time_values.append(deepcopy(expected_current))
                    new_values.append(pd.np.nan)

                    previous_time_value = increment_period(
                        previous_time_value, 1, frequency
                    )

                    expected_current = increment_period(expected_current, 1, frequency)
                    expected_next = increment_period(expected_next, 1, frequency)

            # agrega a la lista el nuevo valor, una vez corregido
            new_time_values.append(deepcopy(current_time_value))
            new_values.append(deepcopy(current_value))

            # incrementa los valores anteriores, para la próxima iteración
            previous_time_value = deepcopy(current_time_value)
            current_time_value = deepcopy(next_time_value)
            current_value = deepcopy(next_value)

    # agrega el último valor, después de las iteraciones
    new_time_values.append(deepcopy(next_time_value))
    new_values.append(deepcopy(next_value))

    new_time_values_str = [value.format("YYYY-MM-DD") for value in new_time_values]

    return new_time_values_str, new_values


def freq_iso_to_pandas(freq_iso8601, how="start"):
    frequencies_map_start = {
        "R/P1Y": "AS",
        "R/P6M": "6MS",
        "R/P3M": "QS",
        "R/P1M": "MS",
        "R/P1D": "D",
    }
    frequencies_map_end = {
        "R/P1Y": "A",
        "R/P6M": "6M",
        "R/P3M": "Q",
        "R/P1M": "M",
        "R/P1D": "D",
    }
    if how == "start":
        return frequencies_map_start[freq_iso8601]
    if how == "end":
        return frequencies_map_end[freq_iso8601]

    raise Exception(
        "{} no se reconoce para 'how': debe ser 'start' o 'end'".format(how)
    )


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logging_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(logging_formatter)
    # logger.addHandler(ch)

    return logger
