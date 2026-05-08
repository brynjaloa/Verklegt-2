from django import forms
from .models import Artwork


class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = [
            "title",
            "category",
            "starting_bid",
            "width",
            "height",
            "year",
            "description",
            "main_image",
            "painting_medium",
            "painting_style",
            "sculpture_material",
            "sculpture_style",
            "furniture_material",
            "furniture_style",
            "photo_technique",
            "photo_style",
            "edition",
            "provenance",
        ]
