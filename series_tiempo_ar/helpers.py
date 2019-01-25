#! coding: utf-8
import logging
import chardet
import csv


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
