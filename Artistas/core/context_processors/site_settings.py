from core.models import SiteSettings


def site_settings(request):
    """
    Hace disponible la configuración global
    del sitio en todos los templates.
    """

    return {
        "site_settings": SiteSettings.objects.first()
    }