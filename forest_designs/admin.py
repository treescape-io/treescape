from django.contrib.gis import admin

from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.GISModelAdmin):
    """Admin inline for Plant model."""

    autocomplete_fields = ("genus", "species")
