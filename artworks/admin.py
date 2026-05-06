from django.contrib import admin
from .models import Artwork, Seller, ArtworkImage

admin.site.register(Seller)
admin.site.register(Artwork)
admin.site.register(ArtworkImage)


