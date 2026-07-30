from django.db import models

from .base import BaseModel
from .artist import Artist

from core.utils.upload_paths import award_image_path

from django.core.exceptions import ValidationError
from django.utils import timezone

from core.utils.date_utils import format_full_date


class Award(BaseModel):


    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="awards"
    )


    name = models.CharField(
        max_length=200
    )


    image = models.ImageField(
        upload_to=award_image_path
    )


    award_date = models.DateField()


    def clean(self):

        if self.award_date > timezone.now().date():

            raise ValidationError(
                "La fecha del premio no puede estar en el futuro."
            )


    description = models.TextField()


    @property
    def formatted_award_date(self):

        return format_full_date(
            self.award_date
        )



    class Meta:

        ordering = [
            "-award_date"
        ]

        verbose_name = "Premio"

        verbose_name_plural = "Premios"



    def __str__(self):

        return self.name