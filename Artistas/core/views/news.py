from django.shortcuts import render, get_object_or_404

from core.models import Artist

from core.services.news_service import get_news_context



def news_list(request, slug):


    artist = get_object_or_404(

        Artist,

        slug=slug

    )


    context = get_news_context(

        artist

    )


    context["current_section"] = "news"


    return render(

        request,

        "core/news.html",

        context

    )