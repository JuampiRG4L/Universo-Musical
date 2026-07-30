from django.contrib import admin

from core.models import SocialLink



class SocialLinkInline(admin.TabularInline):

    model = SocialLink

    extra = 1

    ordering = (

        "display_order",

    )