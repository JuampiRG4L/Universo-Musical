from django.contrib import admin
from django.utils.html import format_html

from core.models import Award



@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):


    list_display = (

        "image_preview",

        "name",

        "artist",

        "formatted_award_date",

        "created_at",

    )


    search_fields = (

        "name",

        "artist__stage_name",

    )


    list_filter = (

        "artist",

        "award_date",

    )


    ordering = (

        "-award_date",

    )


    readonly_fields = (

        "image_preview",

        "created_at",

        "updated_at",

    )


    fieldsets = (


        (
            "Información del premio",

            {

                "fields": (

                    "artist",

                    "name",

                    "award_date",

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
            "Auditoría",

            {

                "fields": (

                    "created_at",

                    "updated_at",

                )

            }

        ),

    )



    @admin.display(description="Imagen")

    def image_preview(self, obj):

        if obj.image:


            return format_html(

                '<img src="{}" width="100" height="80" style="object-fit:cover;border-radius:8px;">',

                obj.image.url

            )


        return "Sin imagen"