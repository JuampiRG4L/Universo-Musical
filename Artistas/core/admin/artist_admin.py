from django.contrib import admin

from core.models import Artist

from .social_admin import SocialLinkInline
from .mixins import ImagePreviewMixin



@admin.register(Artist)
class ArtistAdmin(ImagePreviewMixin, admin.ModelAdmin):


    list_display = (

        "profile_preview",

        "stage_name",

        "full_name",

        "country",

        "formatted_birth_date",

        "created_at",

    )


    search_fields = (

        "stage_name",

        "full_name",

    )


    list_filter = (

        "country",

    )


    readonly_fields = (

        "profile_preview",

        "created_at",

        "updated_at",

    )


    prepopulated_fields = {

        "slug": (

            "stage_name",

        )

    }


    fieldsets = (


        (
            "Información básica",

            {

                "fields": (

                    "stage_name",

                    "full_name",

                    "country",

                    "birth_date",

                )

            }

        ),



        (
            "Biografía",

            {

                "fields": (

                    "short_biography",

                    "biography",

                )

            }

        ),



        (
            "Imágenes",

            {

                "fields": (

                    "profile_image",

                    "profile_preview",

                    "favicon",

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

        SocialLinkInline,

    ]



    @admin.display(description="Imagen")
    def profile_preview(self, obj):

        return self.image_preview(

            obj.profile_image,

            width=80,

            height=80

        )