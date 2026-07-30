from core.selectors.artist_selector import get_home_artists


def get_home_context():

    return {

        "artists": get_home_artists(),

    }