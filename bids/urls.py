from django.urls import path
from . import views

urlpatterns = [

    path(
        'cancel/<int:bid_id>/',
        views.cancel_bid,
        name='cancel_bid'
    ),
]