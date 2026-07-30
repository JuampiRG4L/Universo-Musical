from django.shortcuts import render

from core.services.album_service import get_album_context


def album_detail(request, slug):

    context = get_album_context(slug)

    context["current_section"] = "album"

    return render(

        request,

        "core/album.html",

        context

    )