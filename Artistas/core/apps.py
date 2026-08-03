from django.apps import AppConfig


class CoreConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"

    name = "core"

    def ready(self):
        from django.db.models.signals import post_save, post_delete
        from django.core.cache import cache

        from core.models import SiteSettings
        from core.context_processors.site_settings import SITE_SETTINGS_CACHE_KEY

        def invalidate_site_settings_cache(**kwargs):
            cache.delete(SITE_SETTINGS_CACHE_KEY)

        post_save.connect(invalidate_site_settings_cache, sender=SiteSettings)
        post_delete.connect(invalidate_site_settings_cache, sender=SiteSettings)
