from io import BytesIO
from pathlib import Path
from typing import Any, Optional
from typing_extensions import TypeAlias
from django import forms
from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError
from .models import Artwork



CategoryFields: TypeAlias = dict[str, tuple[str, str]]

CATEGORY_SPECIFIC_FIELDS: CategoryFields = {
    Artwork.Category.PAINTINGS.value: ("painting_medium", "painting_style"),
    Artwork.Category.SCULPTURES.value: ("sculpture_material", "sculpture_style"),
    Artwork.Category.FURNITURE.value: ("furniture_material", "furniture_style"),
    Artwork.Category.PHOTOS.value: ("photo_technique", "photo_style"),
}


def clear_irrelevant_category_fields(cleaned_data: Optional[dict[str, Any]]) -> dict[str, Any]:
    cleaned_data = cleaned_data or {}
    selected_category = cleaned_data.get("category")
    allowed_fields = set()

    if isinstance(selected_category, str):
        allowed_fields.update(CATEGORY_SPECIFIC_FIELDS.get(selected_category, ()))

    for field_names in CATEGORY_SPECIFIC_FIELDS.values():
        for field_name in field_names:
            if field_name not in allowed_fields:
                cleaned_data[field_name] = None

    return cleaned_data


def clear_irrelevant_dimension_fields(cleaned_data: dict[str, Any] | None) -> dict[str, Any]:
    cleaned_data = cleaned_data or {}

    if cleaned_data.get("category") != Artwork.Category.FURNITURE.value:
        cleaned_data["depth"] = None

    return cleaned_data


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if not data and self.required:
            raise forms.ValidationError("Upload at least one additional picture.")

        if not data:
            return []

        if not isinstance(data, (list, tuple)):
            data = [data]

        return [super(MultipleImageField, self).clean(file, initial) for file in data]


class ArtworkForm(forms.ModelForm):
    main_image = forms.ImageField(
        required=True,
        label="Main picture",
    )
    second_image = forms.ImageField(
        required=True,
        label="Second picture",
        help_text="A listing must have at least 2 pictures.",
    )
    additional_images = MultipleImageField(
        required=False,
        label="More pictures",
        help_text="Optional: select one or more extra pictures.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["main_image"].required = not bool(self.instance and self.instance.main_image)
        self.fields["second_image"].required = not bool(self.instance and self.instance.pk)
        self.fields["width"].required = False
        self.fields["height"].required = False
        self.fields["depth"].required = False
        self.fields["width"].help_text = "Recommended"
        self.fields["height"].help_text = "Recommended"
        self.fields["depth"].help_text = "Recommended for furniture"

    @staticmethod
    def clean_image_file(image: Any) -> Any:
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

    def clean_main_image(self):
        return self.clean_image_file(self.cleaned_data.get("main_image"))

    def clean_second_image(self):
        return self.clean_image_file(self.cleaned_data.get("second_image"))

    def clean_additional_images(self):
        images = self.cleaned_data.get("additional_images", [])

        return [self.clean_image_file(image) for image in images]

    def clean(self):
        cleaned_data = clear_irrelevant_category_fields(super().clean())
        cleaned_data = clear_irrelevant_dimension_fields(cleaned_data)

        return cleaned_data

    class Meta:
        model = Artwork
        fields = [
            "title",
            "category",
            "starting_bid",
            "width",
            "height",
            "depth",
            "year",
            "description",
            "main_image",
            "second_image",
            "additional_images",
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
