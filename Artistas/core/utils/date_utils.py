from django.utils.formats import date_format


def format_full_date(date_value):
    """
    Devuelve una fecha en formato:
    26 de julio de 2026

    Si la fecha es None devuelve una cadena vacía.
    """

    if not date_value:
        return ""

    return date_format(
        date_value,
        r"j \d\e F \d\e Y"
    )