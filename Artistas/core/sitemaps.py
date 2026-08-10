from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from core.models import Album, Artist


class ArtistSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Artist.objects.order_by("stage_name")

    def lastmod(self, obj):
        return obj.updated_at


class AlbumSitemap(Sitemap):

    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Album.objects.select_related("artist").order_by("title")

    def lastmod(self, obj):
        return obj.updated_at


class StaticViewSitemap(Sitemap):

    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)
