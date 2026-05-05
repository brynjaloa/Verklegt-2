from django.db import models
from django.contrib.auth.models import User #built in fall sem sér um helstu upplýsingar: password, email og stuffs

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username
