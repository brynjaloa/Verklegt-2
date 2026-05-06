from django.db import models
from accounts.models import Seller

class Artwork(models.Model):
    class Category(models.TextChoices):
        FURNITURE = "Furniture", "Furniture"
        PAINTINGS = "Paintings", "Paintings"
        SCULPTURES = "Sculptures", "Sculptures"
        PHOTOS = "Photos", "Photos"

    class PaintingMedium(models.TextChoices):
        OIL = "Oil", "Oil"
        WATER = "Water", "Water"
        ACRYLIC = "Acrylic", "Acrylic"
        OTHER = "Other", "Other"

    class SculptureMaterial(models.TextChoices):
        BRONZE = "Bronze", "Bronze"
        MARBLE = "Marble", "Marble"
        WOOD = "Wood", "Wood"
        CLAY = "Clay", "Clay"
        OTHER = "Other", "Other"

    class FurnitureMaterial(models.TextChoices):
        WOOD = "Wood", "Wood"
        METAL = "Metal", "Metal"
        GLASS = "Glass", "Glass"
        OTHER = "Other", "Other"

    class PhotoTechnique(models.TextChoices):
        DIGITAL = "Digital", "Digital"
        FILM = "Film", "Film"
        BLACK_AND_WHITE = "Black & White", "Black & White"
        OTHER = "Other", "Other"

    class PaintingStyle(models.TextChoices):
        IMPRESSIONISM = 'Impressionism', 'Impressionism'
        MODERNISM = 'Modernism', 'Modernism'
        SURREALISM = 'Surrealism', 'Surrealism'
        REALISM = 'Realism', 'Realism'
        OTHER = 'Other', 'Other'

    class SculptureStyle(models.TextChoices):
        ABSTRACT = 'Abstract', 'Abstract'
        FIGURATIVE = 'Figurative', 'Figurative'
        MINIMALIST = 'Minimalist', 'Minimalist'
        CONTEMPORARY = 'Contemporary', 'Contemporary'
        OTHER = 'Other', 'Other'

    class FurnitureStyle(models.TextChoices):
        VICTORIAN = 'Victorian', 'Victorian'
        ART_DECO = 'Art Deco', 'Art Deco'
        MODERN = 'Modern', 'Modern'
        MINIMALIST = 'Minimalist', 'Minimalist'
        OTHER = 'Other', 'Other'

    class PhotoStyle(models.TextChoices):
        PORTRAIT = 'Portrait', 'Portrait'
        LANDSCAPE = 'Landscape', 'Landscape'
        STREET = 'Street', 'Street'
        ABSTRACT = 'Abstract', 'Abstract'
        OTHER = 'Other', 'Other'

    class Edition(models.TextChoices):
        ORIGINAL = 'Original', 'Original'
        LIMITED = 'Limited Edition', 'Limited Edition'
        OPEN = 'Open Edition', 'Open Edition'
        OTHER = 'Other', 'Other'

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="artworks")

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=Category.choices)

    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    year = models.IntegerField()

    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to="artworks/", blank=True, null=True)

    painting_medium = models.CharField(max_length=50, choices=PaintingMedium.choices, blank=True, null=True)
    sculpture_material = models.CharField(max_length=50, choices=SculptureMaterial.choices, blank=True, null=True)
    furniture_material = models.CharField(max_length=50, choices=FurnitureMaterial.choices, blank=True, null=True)
    photo_technique = models.CharField(max_length=50, choices=PhotoTechnique.choices, blank=True, null=True)

    painting_style = models.CharField(max_length=50, choices=PaintingStyle.choices, blank=True, null=True)
    sculpture_style = models.CharField(max_length=50, choices=SculptureStyle.choices, blank=True, null=True)
    furniture_style = models.CharField(max_length=50, choices=FurnitureStyle.choices, blank=True, null=True)
    photo_style = models.CharField(max_length=50, choices=PhotoStyle.choices, blank=True, null=True)

    edition = models.CharField(max_length=50, choices=Edition.choices)
    provenance = models.TextField(blank=True, null=True)

    is_sold = models.BooleanField(default=False)
    listing_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="artworks/")

    def __str__(self):
        return f"Image for {self.artwork.title}"

