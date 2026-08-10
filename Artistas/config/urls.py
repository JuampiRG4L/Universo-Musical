from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

from core.sitemaps import AlbumSitemap, ArtistSitemap, StaticViewSitemap

sitemaps = {
    "artists": ArtistSitemap,
    "albums": AlbumSitemap,
    "static": StaticViewSitemap,
}


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "i18n/",
        include("django.conf.urls.i18n")
    ),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap"
    ),

    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ),
        name="robots"
    ),

]


urlpatterns += i18n_patterns(

    path(
        "",
        include("core.urls")
    ),

)


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )