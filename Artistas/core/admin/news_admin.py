from django.contrib import admin
from django.utils.html import format_html

from core.models import News



@admin.register(News)
class NewsAdmin(admin.ModelAdmin):


    list_display = (

        "image_preview",

        "title",

        "artist",

        "category",

        "formatted_publication_date",

        "is_published",

    )


    search_fields = (

        "title",

        "artist__stage_name",

    )


    list_filter = (

        "category",

        "is_published",

        "artist",

    )


    ordering = (

        "-publication_date",

    )


    readonly_fields = (

        "image_preview",

        "created_at",

        "updated_at",

    )


    prepopulated_fields = {

        "slug": (

            "title",

        )

    }


    fieldsets = (


        (
            "Información de la noticia",

            {

                "fields": (

                    "artist",

                    "title",

                    "category",

                    "publication_date",

                    "description",

                    "content",

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
            "Estado",

            {

                "fields": (

                    "is_published",

                )

            }

        ),



        (
            "SEO",

            {

                "fields": (

                    "slug",

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