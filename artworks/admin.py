from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from django.forms.models import BaseInlineFormSet

from accounts.models import Seller
from .forms import clear_irrelevant_category_fields
from .models import Artwork, ArtworkImage


class ArtworkAdminForm(forms.ModelForm):
    def clean(self):
        return clear_irrelevant_category_fields(super().clean())


class ArtworkImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        image_count = 0
        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue

            if form.cleaned_data.get("DELETE"):
                continue

            if form.cleaned_data.get("image"):
                image_count += 1
            elif form.instance.pk and form.instance.image:
                image_count += 1

        if image_count < 2:
            raise ValidationError("Must upload two pictures before posting an artwork.")


class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    formset = ArtworkImageInlineFormSet
    extra = 2
    verbose_name_plural = "Artwork images - must upload two pictures"
    fieldsets = (
        (None, {
            "description": "Must upload two pictures. If the form has errors before saving, choose the image files again.",
            "fields": ("image",),
        }),
    )


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    form = ArtworkAdminForm
    inlines = [ArtworkImageInline]
    fieldsets = (
        (None, {
            "fields": (
                "seller",
                "title",
                "category",
                "starting_bid",
                "width",
                "height",
                "depth",
                "year",
                "description",
                "painting_medium",
                "sculpture_material",
                "furniture_material",
                "photo_technique",
                "painting_style",
                "sculpture_style",
                "furniture_style",
                "photo_style",
                "edition",
                "provenance",
                "is_sold",
            ),
        }),
    )
    list_display = ("title", "seller", "category", "starting_bid", "is_sold", "listing_date")
    list_filter = ("category", "is_sold", "listing_date")
    search_fields = ("title", "description", "seller__name")

    class Media:
        js = ("artworks/admin_artwork_form.js",)


admin.site.register(Seller)
