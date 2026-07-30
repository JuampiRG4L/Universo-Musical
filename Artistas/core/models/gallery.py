from django.db import models

from .base import BaseModel
from .artist import Artist

from core.utils.upload_paths import gallery_image_path


class GalleryImage(BaseModel):

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="gallery"
    )


    title = models.CharField(
        max_length=150
    )


    image = models.ImageField(
        upload_to=gallery_image_path
    )


    description = models.TextField(
        blank=True
    )


    display_order = models.PositiveIntegerField(
        default=1
    )


    is_featured = models.BooleanField(
        default=False
    )


    class Meta:

        ordering = [
            "display_order"
        ]

        verbose_name = "Imagen de galería"

        verbose_name_plural = "Galería"


    def __str__(self):

        return self.title