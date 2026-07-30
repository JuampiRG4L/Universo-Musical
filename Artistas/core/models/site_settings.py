from django.db import models

from .base import BaseModel

from core.utils.upload_paths import (
    site_logo_path,
    site_favicon_path,
)


class SiteSettings(BaseModel):


    site_name = models.CharField(
        max_length=100,
        default="Universo Musical"
    )


    logo = models.ImageField(
        upload_to=site_logo_path
    )


    favicon = models.ImageField(
        upload_to=site_favicon_path
    )


    description = models.TextField()


    footer_text = models.CharField(
        max_length=200,
        default="Todos los derechos reservados"
    )


    class Meta:

        verbose_name = "Configuración del sitio"

        verbose_name_plural = "Configuración del sitio"



    def __str__(self):

        return self.site_name