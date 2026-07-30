from core.selectors.news_selector import get_artist_news



def get_news_context(artist):

    return {


        "artist": artist,


        "news": get_artist_news(artist),


    }