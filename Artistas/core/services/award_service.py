from core.selectors.award_selector import get_artist_awards



def get_award_context(artist):

    return {


        "artist": artist,


        "awards": get_artist_awards(artist),


    }