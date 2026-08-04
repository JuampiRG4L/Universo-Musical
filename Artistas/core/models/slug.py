from django.db import models
from django.utils.text import slugify


class SlugModel(models.Model):

    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True
    )

    class Meta:

        abstract = True

    def generate_slug(self):

        return slugify(
            self.get_slug_text()
        )

    def get_unique_slug(self):

        base_slug = self.generate_slug()
        slug = base_slug
        suffix = 2

        ModelClass = self.__class__

        while (
            ModelClass.objects
            .filter(slug=slug)
            .exclude(pk=self.pk)
            .exists()
        ):
            slug = f"{base_slug}-{suffix}"
            suffix += 1

        return slug

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = self.get_unique_slug()

        super().save(*args, **kwargs)

    def get_slug_text(self):

        raise NotImplementedError(
            "Debes definir get_slug_text()"
        )