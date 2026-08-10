from core.selectors.artist_selector import search_artists


def get_search_context(query):

    return {
        "query": query,
        "artists": search_artists(query),
    }
