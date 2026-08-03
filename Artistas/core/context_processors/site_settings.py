from django.core.cache import cache

from core.models import SiteSettings

SITE_SETTINGS_CACHE_KEY = "site_settings"
SITE_SETTINGS_CACHE_TTL = 60 * 15  # 15 minutos


def site_settings(request):
    """
    Hace disponible la configuración global
    del sitio en todos los templates, cacheada para
    no consultar la base de datos en cada request.
    """

    settings_obj = cache.get(SITE_SETTINGS_CACHE_KEY)

    if settings_obj is None:
        settings_obj = SiteSettings.objects.first()
        cache.set(SITE_SETTINGS_CACHE_KEY, settings_obj, SITE_SETTINGS_CACHE_TTL)

    return {
        "site_settings": settings_obj
    }
