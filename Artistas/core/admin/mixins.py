from django.utils.html import format_html



class ImagePreviewMixin:


    def image_preview(self, image, width=100, height=80):


        if image:


            return format_html(

                '<img src="{}" width="{}" height="{}" style="object-fit:cover;border-radius:8px;">',

                image.url,

                width,

                height

            )


        return "Sin imagen"