from django.contrib import admin
from .models import Artwork


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "starting_bid", "year", "status")
    list_filter = ("category", "status")
    search_fields = ("title", "description")
