from django.contrib import admin
from django.utils.html import format_html

from core.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "logo_preview",
        "site_name",
    )

    readonly_fields = (
        "logo_preview",
        "favicon_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Información general",
            {
                "fields": (
                    "site_name",
                    "description",
                )
            },
        ),

        (
            "Identidad visual",
            {
                "fields": (
                    "logo",
                    "logo_preview",
                    "favicon",
                    "favicon_preview",
                )
            },
        ),

        (
            "Pie de página",
            {
                "fields": (
                    "footer_text",
                )
            },
        ),

        (
            "Auditoría",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),

    )

    @admin.display(description="Logo")
    def logo_preview(self, obj):

        if obj.logo:

            return format_html(
                '<img src="{}" width="120" style="border-radius:8px;">',
                obj.logo.url,
            )

        return "Sin logo"

    @admin.display(description="Favicon")
    def favicon_preview(self, obj):

        if obj.favicon:

            return format_html(
                '<img src="{}" width="32" height="32">',
                obj.favicon.url,
            )

        return "Sin favicon"