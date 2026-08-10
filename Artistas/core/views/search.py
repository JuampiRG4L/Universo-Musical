from django.shortcuts import render

from core.services.search_service import get_search_context


def search(request):

    query = request.GET.get("q", "").strip()

    context = get_search_context(query)

    context["current_section"] = "search"

    return render(
        request,
        "core/search.html",
        context
    )
