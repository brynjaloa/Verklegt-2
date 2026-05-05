from django.db import models

class Artwork(models.Model):
    title = models.CharField(max_length=100)
    medium = models.CharField(max_length=50)
    style = models.CharField(max_length=50)
    starting_bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    width_cm = models.DecimalField(max_digits=6, decimal_places=2)
    height_cm = models.DecimalField(max_digits=6, decimal_places=2)
    year_created = models.IntegerField()
    is_sold = models.BooleanField(default=False)
    main_image = models.ImageField(upload_to="artworks/", blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


# then: python manage.py makemigrations
# python manage.py migrate