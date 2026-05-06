# users/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Seller(models.Model):
    class SellerType(models.TextChoices):
        INDIVIDUAL = "Individual", "Individual"
        GALLERY = "Gallery", "Gallery"

    name = models.CharField(max_length=255)
    seller_type = models.CharField(max_length=20, choices=SellerType.choices)
    bio = models.TextField(blank=True)
    logo = models.ImageField(upload_to="sellers/logos/", blank=True, null=True)
    cover_image = models.ImageField(upload_to="sellers/covers/", blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    street_name = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name