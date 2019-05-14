from six import text_type

from series_tiempo_ar import custom_exceptions as ce


def validate_distinct_scraping_start_cells(distrib_meta):
    for field in distrib_meta.get("field"):
        if field.get("scrapingIdentifierCell") == field.get("scrapingDataStartCell"):
            raise ce.ScrapingStartCellsIdenticalError(
                field.get("scrapingIdentifierCell"), field.get("scrapingDataStartCell")
            )


def validate_header_cell_field_id(xl, worksheet, headers_coord, headers_value):
    # Las celdas de los headers deben estar en blanco o contener un id
    for header_coord, header_value in zip(headers_coord, headers_value):
        ws_header_value = xl.wb[worksheet][header_coord].value
        if ws_header_value != header_value:
            raise ce.HeaderIdError(
                worksheet, header_coord, header_value, ws_header_value
            )


def validate_header_cell_field_id_or_blank(xl, worksheet, headers_coord, headers_value):
    # Las celdas de los headers deben estar en blanco o contener un id
    for header_coord, header_value in zip(headers_coord, headers_value):
        ws_header_value = xl.wb[worksheet][header_coord].value
        if (
            ws_header_value
            and text_type(ws_header_value).strip()
            and ws_header_value != header_value
        ):
            raise ce.HeaderNotBlankOrIdError(
                worksheet, header_coord, header_value, ws_header_value
            )
