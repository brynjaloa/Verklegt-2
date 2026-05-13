from django.urls import path
from . import views

urlpatterns = [

    path('cancel/<int:bid_id>/',views.cancel_bid,name='cancel_bid'),
    path('<int:bid_id>/accept/',views.accept_bid,name='accept_bid'),
    path('<int:bid_id>/reject/',views.reject_bid,name='reject_bid'),
    path('<int:bid_id>/contingent/',views.contingent_bid,name='contingent_bid'),
    path('<int:bid_id>/finalize/',views.finalize_bid,name='finalize_bid'),
    path('<int:bid_id>/finalize/<str:step>/',views.finalize_bid,name='finalize_bid_step'),
]
