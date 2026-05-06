from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("artworks/", include("artworks.urls")),

    path('accounts/', include('accounts.urls')),

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
