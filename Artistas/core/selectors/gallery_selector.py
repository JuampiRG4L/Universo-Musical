from core.models import GalleryImage


def get_artist_gallery(artist):

    return (

        GalleryImage.objects

        .filter(
            artist=artist
        )

        .order_by(
            "display_order"
        )

    )