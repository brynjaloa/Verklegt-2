from django.db import models
from django.contrib.auth.models import User


class Seller(models.Model):
    class SellerType(models.TextChoices):
        INDIVIDUAL = 'Individual', 'Individual'
        GALLERY = 'Gallery', 'Gallery'

    name = models.CharField(max_length=255)
    seller_type = models.CharField(max_length=20, choices=SellerType.choices)
    bio = models.TextField()
    logo = models.ImageField(upload_to='sellers/logos/')
    cover_image = models.ImageField(upload_to='sellers/covers/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Birtist bara ef notandi er "Gallery"
    street_name = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class Artwork(models.Model):

    class Category(models.TextChoices):
        FURNITURE = 'Furniture', 'Furniture'
        PAINTINGS = 'Paintings', 'Paintings'
        SCULPTURES = 'Sculptures', 'Sculptures'
        PHOTOS = 'Photos', 'Photos'
        JEWELLERY = 'Jewellery', 'Jewellery'

    class PaintingMedium(models.TextChoices):
        OIL = 'Oil', 'Oil'
        WATER = 'Water', 'Water'
        ACRYLIC = 'Acrylic', 'Acrylic'
        OTHER = 'Other', 'Other'

    class SculptureMaterial(models.TextChoices):
        BRONZE = 'Bronze', 'Bronze'
        MARBLE = 'Marble', 'Marble'
        WOOD = 'Wood', 'Wood'
        CLAY = 'Clay', 'Clay'
        OTHER = 'Other', 'Other'

    class FurnitureMaterial(models.TextChoices):
        WOOD = 'Wood', 'Wood'
        METAL = 'Metal', 'Metal'
        GLASS = 'Glass', 'Glass'
        OTHER = 'Other', 'Other'

    class PhotoTechnique(models.TextChoices):
        DIGITAL = 'Digital', 'Digital'
        FILM = 'Film', 'Film'
        BLACK_AND_WHITE = 'Black & White', 'Black & White'
        OTHER = 'Other', 'Other'

    class JewelleryMaterial(models.TextChoices):
        GOLD = 'Gold', 'Gold'
        SILVER = 'Silver', 'Silver'
        DIAMOND = 'Diamond', 'Diamond'
        PLATINUM = 'Platinum', 'Platinum'
        OTHER = 'Other', 'Other'

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

    class JewelleryStyle(models.TextChoices):
        CLASSIC = 'Classic', 'Classic'
        MODERN = 'Modern', 'Modern'
        VINTAGE = 'Vintage', 'Vintage'
        HANDMADE = 'Handmade', 'Handmade'
        OTHER = 'Other', 'Other'

    class Edition(models.TextChoices):
        ORIGINAL = 'Original', 'Original'
        LIMITED = 'Limited Edition', 'Limited Edition'
        OPEN = 'Open Edition', 'Open Edition'
        OTHER = 'Other', 'Other'

    class Status(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        SOLD = 'Sold', 'Sold'

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=Category.choices)
    painting_medium = models.CharField(max_length=50, choices=PaintingMedium.choices, blank=True, null=True)
    sculpture_material = models.CharField(max_length=50, choices=SculptureMaterial.choices, blank=True, null=True)
    furniture_material = models.CharField(max_length=50, choices=FurnitureMaterial.choices, blank=True, null=True)
    photo_technique = models.CharField(max_length=50, choices=PhotoTechnique.choices, blank=True, null=True)
    jewellery_material = models.CharField(max_length=50, choices=JewelleryMaterial.choices, blank=True, null=True)
    painting_style = models.CharField(max_length=50, choices=PaintingStyle.choices, blank=True, null=True)
    sculpture_style = models.CharField(max_length=50, choices=SculptureStyle.choices, blank=True, null=True)
    furniture_style = models.CharField(max_length=50, choices=FurnitureStyle.choices, blank=True, null=True)
    photo_style = models.CharField(max_length=50, choices=PhotoStyle.choices, blank=True, null=True)
    jewellery_style = models.CharField(max_length=50, choices=JewelleryStyle.choices, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    year = models.IntegerField()
    edition = models.CharField(max_length=50, choices=Edition.choices)
    provenance = models.TextField(blank=True, null=True)
    listing_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default='Available')


    def __str__(self):
        return self.title

class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='artworks/')

    def __str__(self):
        return f"Image for {self.artwork.title}"
