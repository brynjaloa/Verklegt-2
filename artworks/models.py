from django.db import models
from accounts.models import Seller

class Artwork(models.Model):
    class Category(models.TextChoices):
        FURNITURE = "Furniture", "Furniture"
        PAINTINGS = "Paintings", "Paintings"
        SCULPTURES = "Sculptures", "Sculptures"
        PHOTOS = "Photos", "Photos"

    class PaintingMedium(models.TextChoices):
        OIL = "Oil painting", "Oil painting"
        WATERCOLOR = "Watercolor painting", "Watercolor painting"
        ACRYLIC = "Acrylic painting", "Acrylic painting"
        GOUACHE = "Gouache", "Gouache"
        ENCAUSTIC = "Encaustic", "Encaustic"
        TEMPERA = "Tempera", "Tempera"
        FRESCO = "Fresco", "Fresco"
        INK = "Ink", "Ink"
        CHARCOAL = "Charcoal", "Charcoal"
        CHALK = "Chalk", "Chalk"
        GRAPHITE = "Graphite", "Graphite"
        SPRAY_PAINTING = "Spray Painting", "Spray Painting"
        OTHER = "Other", "Other"

    class SculptureMaterial(models.TextChoices):
        BRONZE = "Bronze", "Bronze"
        MARBLE = "Marble", "Marble"
        WOOD = "Wood", "Wood"
        CLAY = "Clay", "Clay"
        OTHER = "Other", "Other"

    class FurnitureMaterial(models.TextChoices):
        TEXTILE = "Textile", "Textile"
        WOOD = "Wood", "Wood"
        METAL = "Metal", "Metal"
        PLASTIC = "Plastic", "Plastic"
        LEATHER = "Leather", "Leather"
        ARTIFICIAL_LEATHER = "Artificial leather", "Artificial leather"
        GLASS = "Glass", "Glass"
        STEEL = "Steel", "Steel"
        CONCRETE = "Concrete", "Concrete"
        MARBLE = "Marble", "Marble"
        BRONZE = "Bronze", "Bronze"
        STONE = "Stone", "Stone"
        OTHER = "Other", "Other"

    class PhotoTechnique(models.TextChoices):
        DIGITAL = "Digital", "Digital"
        FILM = "Film", "Film"
        OTHER = "Other", "Other"

    class PaintingStyle(models.TextChoices):
        RENAISSANCE = "Renaissance", "Renaissance"
        BAROQUE = "Baroque", "Baroque"
        ROCOCO = "Rococo", "Rococo"
        NEOCLASSICISM = "Neoclassicism", "Neoclassicism"
        ROMANTICISM = "Romanticism", "Romanticism"
        REALISM = "Realism", "Realism"
        IMPRESSIONISM = "Impressionism", "Impressionism"
        POST_IMPRESSIONISM = "Post-Impressionism", "Post-Impressionism"
        EXPRESSIONISM = "Expressionism", "Expressionism"
        FAUVISM = "Fauvism", "Fauvism"
        CUBISM = "Cubism", "Cubism"
        SURREALISM = "Surrealism", "Surrealism"
        ABSTRACT_ART = "Abstract Art", "Abstract Art"
        FUTURISM = "Futurism", "Futurism"
        POP_ART = "Pop Art", "Pop Art"
        MINIMALISM = "Minimalism", "Minimalism"
        PHOTOREALISM = "Photorealism", "Photorealism"
        CONTEMPORARY_ART = "Contemporary art", "Contemporary art"
        MODERNISM = "Modernism", "Modernism"
        OTHER = "Other", "Other"

    class SculptureStyle(models.TextChoices):
        ABSTRACT = "Abstract", "Abstract"
        LAND = "Land", "Land"
        RELIEF = "Relief", "Relief"
        FREESTANDING = "Freestanding", "Freestanding"
        CARVED = "Carved", "Carved"
        MODELING = "Modeling", "Modeling"
        ASSEMBLED = "Assembled", "Assembled"
        CAST = "Cast", "Cast"
        MINIMALISM = "Minimalism", "Minimalism"
        CONSTRUCTIVISM = "Constructivism", "Constructivism"
        SURREALISM = "Surrealism", "Surrealism"
        KINETIC_ART = "Kinetic Art", "Kinetic Art"
        CONTEMPORARY = "Contemporary", "Contemporary"
        FIGURATIVE_ART = "Figurative Art", "Figurative Art"
        MODERN_ART = "Modern art", "Modern art"
        MODERNISM = "Modernism", "Modernism"
        CUBISM = "Cubism", "Cubism"
        BAROQUE = "Baroque", "Baroque"
        RENAISSANCE = "Renaissance", "Renaissance"
        EXPRESSIONISM = "Expressionism", "Expressionism"
        CLASSICISM = "Classicism", "Classicism"
        HYPERREALISM = "Hyperrealism", "Hyperrealism"
        CONCRETE_ART = "Concrete art", "Concrete art"
        FUTURISM = "Futurism", "Futurism"
        GOTHIC_ART = "Gothic art", "Gothic art"
        OTHER = "Other", "Other"

    class FurnitureStyle(models.TextChoices):
        CONTEMPORARY = "Contemporary", "Contemporary"
        ART_DECO = "Art Deco", "Art Deco"
        MINIMALISM = "Minimalism", "Minimalism"
        RENAISSANCE = "Renaissance", "Renaissance"
        MODERNISM = "Modernism", "Modernism"
        BAROQUE = "Baroque", "Baroque"
        MAXIMALISM = "Maximalism", "Maximalism"
        CLASSICISM = "Classicism", "Classicism"
        POST_MODERNISM = "Post modernism", "Post modernism"
        OTHER = "Other", "Other"

    class PhotoStyle(models.TextChoices):
        LANDSCAPE = "Landscape", "Landscape"
        PORTRAIT = "Portrait", "Portrait"
        FASHION = "Fashion", "Fashion"
        BLACK_AND_WHITE = "Black and white", "Black and white"
        ASTROPHOTOGRAPHY = "Astrophotography", "Astrophotography"
        AERIAL = "Aerial", "Aerial"
        EDITORIAL = "Editorial", "Editorial"
        FOOD = "Food", "Food"
        ARCHITECTURAL = "Architectural", "Architectural"
        HEADSHOT = "Headshot", "Headshot"
        NATURE = "Nature", "Nature"
        SPORTS = "Sports", "Sports"
        CONCEPTUAL = "Conceptual", "Conceptual"
        ABSTRACT = "Abstract", "Abstract"
        OTHER = "Other", "Other"

    class Edition(models.TextChoices):
        ORIGINAL = 'Original', 'Original'
        LIMITED = 'Limited Edition', 'Limited Edition'
        OPEN = 'Open Edition', 'Open Edition'
        OTHER = 'Other', 'Other'

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="artworks")

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=Category.choices)

    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    depth = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
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

    @property
    def primary_image(self):
        if self.main_image:
            return self.main_image

        if not self.pk:
            return None

        first_image = self.images.first()
        if first_image:
            return first_image.image

        return None

    @property
    def display_medium(self):
        medium_fields = {
            self.Category.PAINTINGS: self.painting_medium,
            self.Category.SCULPTURES: self.sculpture_material,
            self.Category.FURNITURE: self.furniture_material,
            self.Category.PHOTOS: self.photo_technique,
        }

        medium = medium_fields.get(self.category)

        if not medium:
            return "Not specified"

        return self._clean_medium_label(medium)

    @staticmethod
    def _clean_medium_label(medium):
        labels_to_remove = (" painting", " Painting", " sculpture", " Sculpture")

        for label in labels_to_remove:
            if medium.endswith(label):
                return medium[:-len(label)]

        return medium

    @property
    def dimensions_display(self):
        dimensions = [
            self._format_dimension(value)
            for value in (self.width, self.height, self.depth)
            if value is not None
        ]

        if not dimensions:
            return "Not specified"

        return " x ".join(dimensions) + " cm"

    @staticmethod
    def _format_dimension(value):
        formatted_value = f"{value.normalize():f}".rstrip("0").rstrip(".")
        return formatted_value or "0"

    @property
    def status_display(self):
        if self.is_sold:
            return "Sold"

        return "Available"

    def __str__(self):
        return self.title


class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="artworks/")

    def __str__(self):
        return f"Image for {self.artwork.title}"
