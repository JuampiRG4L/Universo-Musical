from core.models import Award



def get_artist_awards(artist):

    return (

        Award.objects

        .filter(

            artist=artist

        )

        .order_by(

            "-award_date"

        )

    )