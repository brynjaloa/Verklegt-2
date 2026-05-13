"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from artworks.views import home_view
from .views import info_article_view, info_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("artworks/", include("artworks.urls")),
    path('', include('accounts.urls')),
    path("faq/", TemplateView.as_view(template_name="faq.html"), name="faq"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("location/", TemplateView.as_view(template_name="location.html"), name="location"),
    path("info/", info_view, name="info"),
    path("info/<slug:slug>/", info_article_view, name="info_article"),
    path('bids/', include('bids.urls')),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

