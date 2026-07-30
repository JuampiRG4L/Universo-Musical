from django.urls import path

from .views.home import home
from .views.artist import artist_detail
from .views.album import album_detail
from .views.gallery import gallery
from .views.news import news_list
from .views.award import awards


urlpatterns = [

    path(
        "",
        home,
        name="home"
    ),


    path(
        "artista/<slug:slug>/",
        artist_detail,
        name="artist_detail"
    ),


    path(
        "album/<slug:slug>/",
        album_detail,
        name="album_detail",
    ),


    path(
        "artista/<slug:slug>/galeria/",
        gallery,
        name="artist_gallery"
    ),


    path(
        "artista/<slug:slug>/noticias/",
        news_list,
        name="artist_news"
    ),


    path(
        "artista/<slug:slug>/premios/",
        awards,
        name="artist_awards"
    ),

]