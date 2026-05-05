from django.contrib import admin
from .models import Artwork


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("title", "medium", "style", "starting_bid_price", "is_sold")
    list_filter = ("medium", "style", "is_sold")
    search_fields = ("title", "description")
