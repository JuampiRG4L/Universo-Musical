from core.selectors.album_selector import get_album


def get_album_context(slug):

    album = get_album(slug)

    return {

        "artist": album.artist,

        "album": album,

        "songs": album.songs.all(),

    }