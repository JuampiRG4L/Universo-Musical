from django.shortcuts import get_object_or_404

from core.models import Artist



def get_home_artists():

    return (

        Artist.objects

        .select_related(
            "country"
        )

        .order_by(
            "stage_name"
        )

    )



def get_artist(slug):

    return get_object_or_404(

        Artist.objects

        .select_related(
            "country"
        )

        .prefetch_related(
            "social_links",
            "albums",
            "gallery",
            "news",
            "awards",
        ),

        slug=slug

    )