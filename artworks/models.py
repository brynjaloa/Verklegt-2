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

    # Only shown if seller_type == Gallery
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

    class Medium(models.TextChoices):
        OIL = 'Oil', 'Oil'
        WATER = 'Water', 'Water'
        ACRYLIC = 'Acrylic', 'Acrylic'

    class Style(models.TextChoices):
        IMPRESSIONISM = 'Impressionism', 'Impressionism'
        MODERNISM = 'Modernism', 'Modernism'
        SURREALISM = 'Surrealism', 'Surrealism'
        REALISM = 'Realism', 'Realism'

    class Edition(models.TextChoices):
        ORIGINAL = 'Original', 'Original'
        LIMITED = 'Limited Edition', 'Limited Edition'
        OPEN = 'Open Edition', 'Open Edition'

    class Status(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        SOLD = 'Sold', 'Sold'

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=Category.choices)
    medium = models.CharField(max_length=50, choices=Medium.choices, blank=True, null=True)
    style = models.CharField(max_length=50, choices=Style.choices, blank=True, null=True)
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
