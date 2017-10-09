#! coding: utf-8

from pydatajson import DataJson


def get_time_series_distributions(catalog):
    """
    Devuelve las distribuciones que tengan un campo de series de tiempo
    Args:
        catalog (str o dict): DataJson o string con ruta o URL a un data.json
    Returns:
        list: lista de identifiers de las distribuciones
    """

    dj = DataJson(catalog)

    distributions = dj.get_distributions()

    def has_time_index(distribution):
        for field in distribution.get('field', []):
            if field.get('specialType') == 'time_index':
                return True
        return False

    return list(filter(has_time_index, distributions))
