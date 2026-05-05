from django.db import models


class Artwork(models.Model):
    class Medium(models.TextChoices):
        OIL = 'Oil', 'Oil'
        WATER = 'Water', 'Water'
        ACRYLIC = 'Acrylic', 'Acrylic'

    class Style(models.TextChoices):
        IMPRESSIONISM = 'Impressionism', 'Impressionism'
        MODERNISM = 'Modernism', 'Modernism'
        SURREALISM = 'Surrealism', 'Surrealism'
        REALISM = 'Realism', 'Realism'

    title = models.CharField(max_length=255)
    medium = models.CharField(max_length=50, choices=Medium.choices, blank=True, null=True)
    style = models.CharField(max_length=50, choices=Style.choices, blank=True, null=True)
    starting_bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    width_cm = models.DecimalField(max_digits=6, decimal_places=2)
    height_cm = models.DecimalField(max_digits=6, decimal_places=2)
    year_created = models.IntegerField()
    is_sold = models.BooleanField(default=False)
    main_image = models.ImageField(upload_to='artworks/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
