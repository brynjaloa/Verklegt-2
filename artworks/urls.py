from django.urls import path
from . import views

urlpatterns = [
    path("", views.artwork_list, name="artwork_list"),
    path("<int:pk>/", views.artwork_detail, name="artwork_detail"),
    path("add/", views.add_artwork, name="add_artwork"),
]