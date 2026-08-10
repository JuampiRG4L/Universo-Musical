from django.shortcuts import get_object_or_404

from core.models import Album


def get_album(slug):

    return get_object_or_404(

        Album.objects

        .select_related(
            "artist"
        )

        .prefetch_related(
            "songs"
        ),

        slug=slug

    )


def get_artist_albums(artist):

    return (

        artist.albums

        .all()

        .order_by(
            "-release_date"
        )

    )