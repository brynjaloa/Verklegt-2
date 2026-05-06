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
            "sculpture_material",
            "furniture_material",
            "photo_technique",
            "style",
        ]