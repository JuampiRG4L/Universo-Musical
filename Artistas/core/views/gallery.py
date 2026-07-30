from django.shortcuts import render, get_object_or_404

from core.models import Artist

from core.services.gallery_service import get_gallery_context



def gallery(request, slug):

    artist = get_object_or_404(

        Artist,

        slug=slug

    )


    context = get_gallery_context(
        artist
    )


    context["current_section"] = "gallery"


    return render(

        request,

        "core/gallery.html",

        context

    )