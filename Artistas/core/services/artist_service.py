from core.selectors.artist_selector import get_artist


def get_artist_context(slug):

    artist = get_artist(slug)

    return {

        "artist": artist,

        "page_favicon": artist.favicon,

        "social_links": artist.social_links.all(),

    }