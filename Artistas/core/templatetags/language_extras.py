from django import template
from django.conf import settings

register = template.Library()


@register.filter
def flag_emoji_for_code(country_code):
    """
    Convierte un código de país ISO 3166 alpha-2 (ej. "CO") en su
    emoji de bandera correspondiente (ej. 🇨🇴). Devuelve cadena vacía
    si no se recibe un código válido.
    """

    if not country_code or len(country_code) != 2:
        return ""

    code = country_code.upper()

    return "".join(
        chr(127397 + ord(letter))
        for letter in code
    )


@register.simple_tag
def language_flag(language_code):
    """
    Devuelve el emoji de bandera configurado para un idioma
    (ver settings.LANGUAGE_COUNTRY_FLAGS). Si el idioma no tiene
    bandera configurada, devuelve cadena vacía sin romper nada.
    """

    country_code = settings.LANGUAGE_COUNTRY_FLAGS.get(language_code, "")

    return flag_emoji_for_code(country_code)


@register.simple_tag
def language_code_label(language_code):
    """
    Devuelve la etiqueta corta a mostrar junto a la bandera
    (el código de país configurado, ej. "CO"). Si el idioma no
    tiene país configurado, cae de vuelta al código de idioma
    en mayúsculas (ej. "ES") para que nunca quede vacío.
    """

    return settings.LANGUAGE_COUNTRY_FLAGS.get(
        language_code,
        language_code.upper()
    )
