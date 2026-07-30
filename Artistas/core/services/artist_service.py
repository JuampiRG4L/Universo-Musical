from core.selectors.artist_selector import get_artist


def get_artist_context(slug):

    artist = get_artist(slug)

    return {

        "artist": artist,

        "page_favicon": artist.favicon,

        "albums": artist.albums.all(),

        "gallery": artist.gallery.all(),

        "news": artist.news.filter(
            is_published=True
        ),

        "awards": artist.awards.all(),

        "social_links": artist.social_links.all(),

    }