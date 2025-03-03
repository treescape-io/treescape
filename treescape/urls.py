"""
URL configuration for treescape project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework.schemas import get_schema_view

from species_data import urls as species_urls
from forest_designs import urls as forest_urls

from .views import index

# Schema view for generating OpenAPI schema
schema_view = get_schema_view(
    title="Treescape API",
    description="API for accessing species data and forest designs",
    version="1.0.0",
    urlconf="treescape.urls",
)

# API v1 url patterns
api_v1_patterns = [
    path("species/", include(species_urls.urlpatterns)),
    path("forest-designs/", include(forest_urls.urlpatterns)),
    
    # Authentication endpoints
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    
    # OpenAPI schema
    path("openapi.xml", schema_view, name="openapi-schema"),
]

urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1_patterns)),
    path("accounts/", include("allauth.urls")),  # Required for social auth callbacks
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
