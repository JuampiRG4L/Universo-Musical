import os

from django.utils.text import slugify

def artist_profile_path(instance, filename):

    extension = filename.split(".")[-1]

    filename = f"profile.{extension}"

    slug = slugify(instance.stage_name)

    return os.path.join(
        "artists",
        slug,
        filename,
    )

def artist_favicon_path(instance, filename):

    extension = filename.split(".")[-1]

    filename = f"favicon.{extension}"

    slug = slugify(instance.stage_name)

    return os.path.join(
        "artists",
        slug,
        filename,
    )

def album_cover_path(instance, filename):

    extension = filename.split(".")[-1]

    filename = f"{slugify(instance.title)}.{extension}"

    artist_slug = slugify(instance.artist.stage_name)

    return os.path.join(
        "artists",
        artist_slug,
        "albums",
        filename,
    )

def gallery_image_path(instance, filename):

    extension = filename.split(".")[-1]

    filename = f"{slugify(instance.title)}.{extension}"

    artist_slug = slugify(instance.artist.stage_name)

    return os.path.join(
        "artists",
        artist_slug,
        "gallery",
        filename,
    )

def news_image_path(instance, filename):

    extension = filename.split(".")[-1]

    filename = f"{slugify(instance.title)}.{extension}"

    artist_slug = slugify(instance.artist.stage_name)

    return os.path.join(
        "artists",
        artist_slug,
        "news",
        filename,
    )

def award_image_path(instance, filename):

    extension = filename.split(".")[-1]

    filename = f"{slugify(instance.name)}.{extension}"

    artist_slug = slugify(instance.artist.stage_name)

    return os.path.join(
        "artists",
        artist_slug,
        "awards",
        filename,
    )

def country_flag_path(instance, filename):

    extension = filename.split(".")[-1]

    filename = f"{slugify(instance.name)}.{extension}"

    return os.path.join(
        "countries",
        filename,
    )

def site_logo_path(instance, filename):

    extension = filename.split(".")[-1]

    return os.path.join(
        "site",
        f"logo.{extension}",
    )


def site_favicon_path(instance, filename):

    extension = filename.split(".")[-1]

    return os.path.join(
        "site",
        f"favicon.{extension}",
    )