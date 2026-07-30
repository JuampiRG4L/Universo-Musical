from django.shortcuts import render, get_object_or_404

from core.models import Artist

from core.services.award_service import get_award_context



def awards(request, slug):


    artist = get_object_or_404(

        Artist,

        slug=slug

    )


    context = get_award_context(

        artist

    )


    context["current_section"] = "awards"


    return render(

        request,

        "core/awards.html",

        context

    )