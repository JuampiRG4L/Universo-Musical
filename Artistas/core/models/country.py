from django.db import models


class Country(models.Model):

    name = models.CharField(
        max_length=100
    )


    code = models.CharField(
        max_length=2,
        unique=True,
        help_text="Código ISO del país. Ejemplo: CO, US, BR"
    )


    flag = models.ImageField(
        upload_to="countries/flags/",
        blank=True,
        null=True
    )


    class Meta:

        verbose_name = "País"

        verbose_name_plural = "Países"


        ordering = [
            "name"
        ]


    def __str__(self):

        return self.name



    @property
    def flag_emoji(self):

        if not self.code:

            return ""


        code = self.code.upper()


        return "".join(

            chr(
                127397 + ord(letter)
            )

            for letter in code

        )