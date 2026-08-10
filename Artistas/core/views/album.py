from django.shortcuts import render, get_object_or_404

from core.models import Artist

from core.services.album_service import get_album_context, get_artist_albums_context


def album_detail(request, slug):

    context = get_album_context(slug)

    context["current_section"] = "album"

    return render(

        request,

        "core/album.html",

        context

    )


def artist_albums(request, slug):

    artist = get_object_or_404(

        Artist,

        slug=slug

    )

    context = get_artist_albums_context(artist)

    context["current_section"] = "albums"

    return render(

        request,

        "core/albums.html",

        context

    )