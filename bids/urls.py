from django.urls import path
from . import views

urlpatterns = [

    path('cancel/<int:bid_id>/',views.cancel_bid,name='cancel_bid'),
    path('<int:bid_id>/accept/',views.accept_bid,name='accept_bid'),
    path('<int:bid_id>/contingent/',views.contingent_bid,name='contingent_bid'),
]
