from django.contrib import admin
from django.utils.html import format_html

from core.models import Album
from .song_admin import SongInline



@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):


    list_display = (

        "cover_preview",

        "title",

        "artist",

        "formatted_release_date",

        "created_at",

    )


    search_fields = (

        "title",

        "artist__stage_name",

    )


    list_filter = (

        "artist",

        "release_date",

    )


    readonly_fields = (

        "cover_preview",

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
            "Información del álbum",

            {

                "fields": (

                    "artist",

                    "title",

                    "release_date",

                    "description",

                )

            }

        ),



        (
            "Portada",

            {

                "fields": (

                    "cover",

                    "cover_preview",

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


    inlines = [

        SongInline,

    ]



    @admin.display(description="Portada")

    def cover_preview(self, obj):

        if obj.cover:


            return format_html(

                '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:8px;">',

                obj.cover.url

            )


        return "Sin portada"