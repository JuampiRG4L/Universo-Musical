from django.db import models

from .base import BaseModel
from .artist import Artist

from core.utils.upload_paths import news_image_path

from .slug import SlugModel

from core.utils.date_utils import format_full_date


class News(BaseModel, SlugModel):


    CATEGORY_CHOICES = (

        ("release", "Lanzamiento"),

        ("concert", "Concierto"),

        ("interview", "Entrevista"),

        ("award", "Reconocimiento"),

        ("other", "Otro"),

    )


    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="news"
    )


    title = models.CharField(
        max_length=200
    )


    image = models.ImageField(
        upload_to=news_image_path
    )


    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other"
    )


    publication_date = models.DateTimeField()


    description = models.TextField()


    content = models.TextField(
        blank=True
    )


    is_published = models.BooleanField(
        default=True
    )


    def get_slug_text(self):

        return self.title


    @property
    def formatted_publication_date(self):

        return format_full_date(
            self.publication_date
        )


    class Meta:

        ordering = [
            "-publication_date"
        ]

        verbose_name = "Noticia"

        verbose_name_plural = "Noticias"


    def __str__(self):

        return self.title