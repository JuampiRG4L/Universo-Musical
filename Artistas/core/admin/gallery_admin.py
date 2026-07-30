from django.contrib import admin
from django.utils.html import format_html

from core.models import GalleryImage



@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):


    list_display = (

        "image_preview",

        "title",

        "artist",

        "display_order",

        "is_featured",

        "created_at",

    )


    search_fields = (

        "title",

        "artist__stage_name",

    )


    list_filter = (

        "artist",

        "is_featured",

    )


    ordering = (

        "artist",

        "display_order",

    )


    readonly_fields = (

        "image_preview",

        "created_at",

        "updated_at",

    )


    fieldsets = (


        (
            "Información",

            {

                "fields": (

                    "artist",

                    "title",

                    "description",

                )

            }

        ),



        (
            "Imagen",

            {

                "fields": (

                    "image",

                    "image_preview",

                )

            }

        ),



        (
            "Configuración",

            {

                "fields": (

                    "display_order",

                    "is_featured",

                )

            }

        ),



        (
            "Auditoría",

            {

                "fields": (

                    "created_at",

                    "updated_at",

                )

            }

        ),

    )



    @admin.display(description="Vista previa")

    def image_preview(self, obj):

        if obj.image:


            return format_html(

                '<img src="{}" width="100" height="80" style="object-fit:cover;border-radius:8px;">',

                obj.image.url

            )


        return "Sin imagen"