from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.contrib.gis.forms.widgets import OSMWidget

from .models import Project, Plant


class GeoAdminMinx:
    formfield_overrides = {
        models.PointField: {"widget": OSMWidget()},
    }


class PlantInline(admin.TabularInline):
    """Admin inline for Plant model."""

    model = Plant
    extra = 1
    autocomplete_fields = ("genus", "species")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin for Project model."""

    list_display = ("name",)
    search_fields = ("name",)

    inlines = (PlantInline,)
