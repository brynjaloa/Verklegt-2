from django.db import models


class Artwork(models.Model):
    title = models.CharField(max_length=255)
    starting_bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    width_cm = models.DecimalField(max_digits=6, decimal_places=2)
    height_cm = models.DecimalField(max_digits=6, decimal_places=2)
    year_created = models.IntegerField()
    is_sold = models.BooleanField(default=False)
    main_image = models.ImageField(upload_to='artworks/', blank=True, null=True)
    description = models.TextField(blank=True)
    furniture_material = models.CharField(max_length=100, blank=True, null=True)
    furniture_style = models.CharField(max_length=100, blank=True, null=True)
    jewellery_material = models.CharField(max_length=100, blank=True, null=True)
    jewellery_style = models.CharField(max_length=100, blank=True, null=True)
    painting_medium = models.CharField(max_length=100, blank=True, null=True)
    painting_style = models.CharField(max_length=100, blank=True, null=True)
    photo_style = models.CharField(max_length=100, blank=True, null=True)
    photo_technique = models.CharField(max_length=100, blank=True, null=True)
    sculpture_material = models.CharField(max_length=100, blank=True, null=True)
    sculpture_style = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title
