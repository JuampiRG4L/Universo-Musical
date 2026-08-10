from core.selectors.album_selector import get_album, get_artist_albums


def get_album_context(slug):

    album = get_album(slug)

    return {

        "artist": album.artist,

        "album": album,

        "songs": album.songs.all(),

    }


def get_artist_albums_context(artist):

    return {

        "artist": artist,

        "albums": get_artist_albums(artist),

    }