from django.db import models

from .base import BaseModel
from .country import Country

from core.utils.upload_paths import (
    artist_profile_path,
    artist_favicon_path,
)

from .slug import SlugModel

from core.utils.date_utils import format_full_date


class Artist(BaseModel, SlugModel):

    stage_name = models.CharField(
        max_length=150
    )


    full_name = models.CharField(
        max_length=150
    )


    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="artists"
    )


    birth_date = models.DateField(
        blank=True,
        null=True
    )


    short_biography = models.TextField()


    biography = models.TextField()


    profile_image = models.ImageField(
        upload_to=artist_profile_path
    )


    favicon = models.ImageField(
        upload_to=artist_favicon_path,
        blank=True,
        null=True
    )


    def get_slug_text(self):

        return self.stage_name


    @property
    def formatted_birth_date(self):

        return format_full_date(
            self.birth_date
        )

    class Meta:

        verbose_name = "Artista"

        verbose_name_plural = "Artistas"


    def __str__(self):

        return self.stage_name