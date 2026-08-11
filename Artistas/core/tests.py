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

    def test_artist_detail_shows_info_but_not_related_sections(self):
        response = self.client.get(
            reverse("artist_detail", kwargs={"slug": self.artist.slug})
        )
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()
        self.assertIn(self.site_settings.site_name, content)
        self.assertIn(self.artist.stage_name, content)

        # Álbumes, galería, noticias y premios ya NO se muestran en la
        # página de artista: viven en sus propias páginas (ver navbar_artist.html)
        self.assertNotIn(self.album.title, content)
        self.assertNotIn(self.gallery_image.title, content)
        self.assertNotIn(self.news.title, content)
        self.assertNotIn(self.award.name, content)

    def test_artist_albums_page_shows_albums(self):
        response = self.client.get(
            reverse("artist_albums", kwargs={"slug": self.artist.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.album.title)

    def test_album_detail_loads(self):
        response = self.client.get(
            reverse("album_detail", kwargs={"slug": self.album.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_artist_gallery_loads_and_shows_gallery(self):
        response = self.client.get(
            reverse("artist_gallery", kwargs={"slug": self.artist.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.gallery_image.title)

    def test_artist_news_loads_and_shows_news(self):
        response = self.client.get(
            reverse("artist_news", kwargs={"slug": self.artist.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news.title)

    def test_artist_awards_loads_and_shows_awards(self):
        response = self.client.get(
            reverse("artist_awards", kwargs={"slug": self.artist.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.award.name)

    def test_navbar_hides_link_to_current_section(self):
        response = self.client.get(
            reverse("artist_gallery", kwargs={"slug": self.artist.slug})
        )
        content = response.content.decode()
        gallery_url = reverse("artist_gallery", kwargs={"slug": self.artist.slug})
        self.assertNotIn(f'href="{gallery_url}"', content)

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


class SearchTests(BaseTestData):
    """
    Prueba la búsqueda de artistas (core/views/search.py).
    """

    def test_search_finds_matching_artist(self):
        response = self.client.get(reverse("search"), {"q": "Prueba"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.artist.stage_name)

    def test_search_is_case_insensitive_and_partial(self):
        response = self.client.get(reverse("search"), {"q": "artista"})
        self.assertContains(response, self.artist.stage_name)

    def test_search_without_query_shows_no_results(self):
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.artist.stage_name)

    def test_search_with_no_matches(self):
        response = self.client.get(reverse("search"), {"q": "xxxxxxxxx"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.artist.stage_name)


class SlugCollisionTests(TestCase):
    """
    Evita que vuelva a pasar desapercibido el bug donde dos registros
    con el mismo nombre generaban el mismo slug y crasheaban con
    IntegrityError al guardar (core/models/slug.py).
    """

    def test_duplicate_artist_names_get_unique_slugs(self):
        country = Country.objects.create(name="Colombia", code="CO")

        artist_1 = Artist.objects.create(
            stage_name="Nombre Repetido",
            full_name="Persona Uno",
            country=country,
        )
        artist_2 = Artist.objects.create(
            stage_name="Nombre Repetido",
            full_name="Persona Dos",
            country=country,
        )
        artist_3 = Artist.objects.create(
            stage_name="Nombre Repetido",
            full_name="Persona Tres",
            country=country,
        )

        slugs = {artist_1.slug, artist_2.slug, artist_3.slug}
        self.assertEqual(
            len(slugs), 3,
            "Los 3 artistas deberían tener slugs distintos entre sí",
        )
        self.assertEqual(artist_1.slug, "nombre-repetido")

    def test_duplicate_album_titles_get_unique_slugs(self):
        country = Country.objects.create(name="Colombia", code="CO")
        artist = Artist.objects.create(
            stage_name="Artista X",
            full_name="Nombre X",
            country=country,
        )

        album_1 = Album.objects.create(
            artist=artist,
            title="Grandes Éxitos",
            release_date=date(2020, 1, 1),
        )
        album_2 = Album.objects.create(
            artist=artist,
            title="Grandes Éxitos",
            release_date=date(2022, 1, 1),
        )

        self.assertNotEqual(album_1.slug, album_2.slug)


class SEOTests(BaseTestData):
    """
    Prueba que sitemap.xml y robots.txt respondan correctamente.
    """

    def test_sitemap_loads(self):
        response = self.client.get(reverse("sitemap"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn(self.artist.get_absolute_url(), content)
        self.assertIn(self.album.get_absolute_url(), content)

    def test_robots_txt_loads_and_references_sitemap(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sitemap:")
        self.assertContains(response, "Disallow: /admin/")


class TranslationTests(BaseTestData):
    """
    Evita que vuelva a pasar desapercibido que las traducciones no
    existían de verdad (sin archivos .po/.mo compilados, Django solo
    cambiaba el prefijo de la URL pero el texto seguía en español
    sin importar el idioma elegido).
    """

    def test_english_actually_translates_text(self):
        response = self.client.get("/en/buscar/")
        self.assertContains(response, "Search artists")
        self.assertNotContains(response, "Buscar artistas")

    def test_portuguese_actually_translates_text(self):
        response = self.client.get("/pt/")
        self.assertContains(response, "Início")

    def test_spanish_is_the_default(self):
        response = self.client.get("/es/buscar/")
        self.assertContains(response, "Buscar artistas")
    """
    Prueba los cambios de estructura de front-end: "Ver más" como
    <button> (no <a>) en las cards, y el selector de idioma con
    bandera + código.
    """

    def test_artist_card_ver_mas_is_a_button(self):
        response = self.client.get(reverse("search"), {"q": "Prueba"})
        content = response.content.decode()
        self.assertIn('class="btn-ver-mas"', content)
        self.assertIn(
            f'data-href="{self.artist.get_absolute_url()}"',
            content,
        )
        self.assertNotIn("onclick=", content)

    def test_album_card_ver_mas_is_a_button(self):
        response = self.client.get(
            reverse("artist_albums", kwargs={"slug": self.artist.slug})
        )
        content = response.content.decode()
        self.assertIn('class="btn-ver-mas"', content)
        self.assertIn(
            f'data-href="{self.album.get_absolute_url()}"',
            content,
        )
        self.assertNotIn("onclick=", content)

    def test_no_inline_javascript_anywhere(self):
        urls_to_check = [
            reverse("home"),
            reverse("artist_detail", kwargs={"slug": self.artist.slug}),
            reverse("artist_albums", kwargs={"slug": self.artist.slug}),
            reverse("album_detail", kwargs={"slug": self.album.slug}),
            reverse("artist_gallery", kwargs={"slug": self.artist.slug}),
            reverse("artist_news", kwargs={"slug": self.artist.slug}),
            reverse("artist_awards", kwargs={"slug": self.artist.slug}),
            reverse("search"),
        ]

        for url in urls_to_check:
            response = self.client.get(url)
            content = response.content.decode()
            self.assertNotIn(
                "onclick=", content,
                f"{url} tiene JS inline (onclick)",
            )

        # El único <script> permitido es el punto de entrada global
        home_content = self.client.get(reverse("home")).content.decode()
        self.assertIn('src="/static/js/main.js"', home_content)
        response = self.client.get(reverse("home"))
        content = response.content.decode()

        from django.conf import settings

        for code, _name in settings.LANGUAGES:
            self.assertIn(f'value="{code}"', content)
            expected_label = settings.LANGUAGE_COUNTRY_FLAGS.get(
                code, code.upper()
            )
            self.assertIn(expected_label, content)