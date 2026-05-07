from io import BytesIO
from pathlib import Path

from django import forms
from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError

from .models import Artwork


class ArtworkForm(forms.ModelForm):
    main_image = forms.ImageField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["main_image"].required = not bool(self.instance and self.instance.main_image)

    def clean_main_image(self):
        image = self.cleaned_data.get("main_image")

        if not image:
            return image

        try:
            with Image.open(image) as img:
                img = img.convert("RGB")
                buffer = BytesIO()
                img.save(buffer, format="JPEG", quality=90)
        except UnidentifiedImageError:
            raise forms.ValidationError("Upload a valid image file.")

        filename = f"{Path(image.name).stem}.jpg"
        return ContentFile(buffer.getvalue(), name=filename)

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
            "painting_style",
            "sculpture_style",
            "furniture_style",
            "photo_style",
            "edition",
            "provenance",
        ]