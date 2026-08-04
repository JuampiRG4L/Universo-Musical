from datetime import date

from django.contrib import admin
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from core.models import (
    Album,
    Artist,
    Award,
    Country,
    GalleryImage,
    News,
    SiteSettings,
    SocialLink,
)


class BaseTestData(TestCase):
    """
    Crea un set mínimo de datos reutilizable para las pruebas
    de vistas y selectors.
    """

    @classmethod
    def setUpTestData(cls):
        cls.country = Country.objects.create(name="Colombia", code="CO")

        cls.artist = Artist.objects.create(
            stage_name="Artista de Prueba",
            full_name="Nombre Completo de Prueba",
            country=cls.country,
            short_biography="Biografía corta",
            biography="Biografía larga",
        )

        cls.site_settings = SiteSettings.objects.create(
            site_name="Universo Musical",
            footer_text="Todos los derechos reservados",
        )

        cls.album = Album.objects.create(
            artist=cls.artist,
            title="Álbum de Prueba",
            release_date=date(2020, 1, 1),
        )

        cls.gallery_image = GalleryImage.objects.create(
            artist=cls.artist,
            title="Foto de Prueba",
            display_order=1,
        )

        cls.news = News.objects.create(
            artist=cls.artist,
            title="Noticia de Prueba",
            description="Descripción",
            is_published=True,
            publication_date=date.today(),
        )

        cls.award = Award.objects.create(
            artist=cls.artist,
            name="Premio de Prueba",
            award_date=date(2019, 1, 1),
        )

        cls.social_link = SocialLink.objects.create(
            artist=cls.artist,
            social_network="instagram",
            url="https://instagram.com/test",
        )


class AdminRegistrationTests(TestCase):
    """
    Evita que vuelva a pasar desapercibido el bug donde ningún modelo
    quedaba registrado en el admin (core/admin.py vs core/admin/ package).
    """

    def test_all_content_models_registered_in_admin(self):
        expected_models = {
            Artist,
            Album,
            GalleryImage,
            News,
            Award,
            SiteSettings,
        }

        registered_models = set(admin.site._registry.keys())

        missing = expected_models - registered_models
        self.assertFalse(
            missing,
            f"Estos modelos no están registrados en el admin: {missing}",
        )


class PageViewsTests(BaseTestData):
    """
    Prueba que las páginas principales del sitio respondan 200
    y que el contexto/HTML resultante sea el esperado.
    """

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_artist_detail_loads_and_shows_related_data(self):
        response = self.client.get(
            reverse("artist_detail", kwargs={"slug": self.artist.slug})
        )
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()
        self.assertIn(self.site_settings.site_name, content)
        self.assertIn(self.gallery_image.title, content)
        self.assertIn(self.news.title, content)
        self.assertIn(self.award.name, content)

    def test_album_detail_loads(self):
        response = self.client.get(
            reverse("album_detail", kwargs={"slug": self.album.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_artist_gallery_loads(self):
        response = self.client.get(
            reverse("artist_gallery", kwargs={"slug": self.artist.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_artist_news_loads(self):
        response = self.client.get(
            reverse("artist_news", kwargs={"slug": self.artist.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_artist_awards_loads(self):
        response = self.client.get(
            reverse("artist_awards", kwargs={"slug": self.artist.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_unpublished_news_is_not_shown(self):
        News.objects.create(
            artist=self.artist,
            title="Noticia sin publicar",
            description="No debería verse",
            is_published=False,
            publication_date=date.today(),
        )

        response = self.client.get(
            reverse("artist_news", kwargs={"slug": self.artist.slug})
        )
        self.assertNotContains(response, "Noticia sin publicar")


class SiteSettingsCacheTests(BaseTestData):
    """
    Verifica que el context processor cachea SiteSettings y que
    la señal en apps.py invalida el cache al guardar/eliminar.
    """

    def setUp(self):
        cache.clear()

    def test_site_settings_is_cached_after_first_request(self):
        self.client.get(reverse("home"))
        self.assertIsNotNone(cache.get("site_settings"))

    def test_cache_is_invalidated_on_save(self):
        self.client.get(reverse("home"))
        self.assertIsNotNone(cache.get("site_settings"))

        self.site_settings.site_name = "Nombre Actualizado"
        self.site_settings.save()

        self.assertIsNone(cache.get("site_settings"))

        response = self.client.get(reverse("home"))
        self.assertContains(response, "Nombre Actualizado")