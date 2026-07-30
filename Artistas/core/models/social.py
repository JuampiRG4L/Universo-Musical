from django.db import models

from .base import BaseModel
from .artist import Artist


class SocialLink(BaseModel):

    SOCIAL_CHOICES = (
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("tiktok", "TikTok"),
        ("x", "X"),
        ("spotify", "Spotify"),
        ("youtube", "YouTube"),
        ("apple_music", "Apple Music"),
        ("deezer", "Deezer"),
        ("soundcloud", "SoundCloud"),
        ("threads", "Threads"),
    )

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="social_links"
    )

    social_network = models.CharField(
        max_length=30,
        choices=SOCIAL_CHOICES
    )

    url = models.URLField()

    display_order = models.PositiveSmallIntegerField(
        default=1
    )

    class Meta:
        ordering = ["display_order"]

        verbose_name = "Red social"

        verbose_name_plural = "Redes sociales"

        constraints = [
            models.UniqueConstraint(
                fields=["artist", "social_network"],
                name="unique_artist_social_network"
            )
        ]

    def __str__(self):
        return f"{self.artist.stage_name} - {self.get_social_network_display()}"