from django.shortcuts import render

from core.services.artist_service import get_artist_context


def artist_detail(request, slug):

    context = get_artist_context(slug)

    context["current_section"] = "artist"

    return render(

        request,

        "core/artist.html",

        context,

    )