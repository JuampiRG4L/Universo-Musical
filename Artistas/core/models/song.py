from django.db import models

from .base import BaseModel

from .album import Album


class Song(BaseModel):


    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="songs"
    )


    title = models.CharField(
        max_length=150
    )


    duration = models.PositiveIntegerField(
        help_text="Duración en segundos"
    )


    youtube_url = models.URLField()


    order = models.PositiveIntegerField(
        default=1
    )


    class Meta:

        ordering = [
            "order"
        ]

        verbose_name = "Canción"

        verbose_name_plural = "Canciones"



    @property
    def duration_formatted(self):

        minutes = self.duration // 60

        seconds = self.duration % 60

        return f"{minutes}:{seconds:02d}"



    def __str__(self):

        return self.title