from django.contrib import admin

from core.models import Song



class SongInline(admin.TabularInline):

    model = Song

    extra = 1

    ordering = (

        "title",

    )