from core.selectors.gallery_selector import get_artist_gallery



def get_gallery_context(artist):

    return {

        "artist": artist,

        "gallery": get_artist_gallery(artist),

    }