from django.shortcuts import render

from core.services.home_service import get_home_context


def home(request):
    context = get_home_context()
    context["current_section"] = "home"
    return render(request, "core/home.html", context)