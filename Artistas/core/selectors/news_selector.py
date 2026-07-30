from core.models import News



def get_artist_news(artist):

    return (

        News.objects

        .filter(

            artist=artist,

            is_published=True

        )

        .order_by(

            "-publication_date"

        )

    )