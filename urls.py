from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("artworks/", include("artworks.urls")),


    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('accounts/', include('accounts.urls')),

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
