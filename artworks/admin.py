from django.contrib import admin
from .models import Artwork


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("title", "starting_bid_price", "year_created", "is_sold")
    list_filter = ("is_sold",)
    search_fields = ("title", "description")
