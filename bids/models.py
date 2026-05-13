from django.db import models
from django.contrib.auth.models import User
from artworks.models import Artwork

class Bid(models.Model):

    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        ACCEPTED = 'Accepted', 'Accepted'
        REJECTED = 'Rejected', 'Rejected'
        CONTINGENT = 'Contingent', 'Contingent'
        FINALIZED = 'Finalized', 'Finalized'
        CANCELED = 'Canceled', 'Canceled'
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Hver setti tilboðið
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE) #Hlekkur að listaverkinu
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()
    date_of_bid = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default='Pending') #getur verið 1 af 3: Pending, Accepted, Rejected
    buyer_accept_notification_seen = models.BooleanField(default=False)
    buyer_reject_notification_seen = models.BooleanField(default=False)
    seller_cancel_notification_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.artwork.title} - {self.bid_price}"
