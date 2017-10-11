#! coding: utf-8
import logging


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
