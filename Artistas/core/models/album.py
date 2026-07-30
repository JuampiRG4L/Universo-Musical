from django.db import models

from .base import BaseModel
from .artist import Artist

from core.utils.upload_paths import album_cover_path

from .slug import SlugModel

from core.utils.date_utils import format_full_date


class Album(BaseModel, SlugModel):

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="albums"
    )


    title = models.CharField(
        max_length=150
    )


    cover = models.ImageField(
        upload_to=album_cover_path
    )


    release_date = models.DateField()


    description = models.TextField()


    def get_slug_text(self):

        return self.title


    @property
    def formatted_release_date(self):

        return format_full_date(
            self.release_date
        )


    class Meta:

        verbose_name = "Álbum"

        verbose_name_plural = "Álbumes"


    def __str__(self):

        return self.title