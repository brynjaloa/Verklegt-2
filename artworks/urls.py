from django.urls import path
from . import views

urlpatterns = [
    path("", views.artwork_list, name="artwork_list"),
    path("<int:pk>/", views.artwork_detail, name="artwork_detail"),
    path("<int:pk>/edit/", views.edit_artwork, name="edit_artwork"),
    path("<int:pk>/delete/", views.delete_artwork, name="delete_artwork"),
    path('categories/', views.category_list, name='category_list'),
    path("add/", views.add_artwork, name="add_artwork"),
    path("see-all/", views.artwork_see_all, name="see_all"),
]
