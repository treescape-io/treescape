from django.contrib.gis import admin

from .models import (
    Plant,
    PlantImage,
    PlantImageKind,
    PlantLog,
    PlantLogKind,
    Zone,
    ZoneKind,
)


@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    list_display = ("plant", "date", "kind")
    search_fields = ("plant__name", "kind__name")
    list_filter = ("date", "kind")


@admin.register(PlantImageKind)
class PlantImageKindAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(PlantLog)
class PlantLogAdmin(admin.ModelAdmin):
    list_display = ("plant", "date", "kind", "notes")
    search_fields = ("plant__name", "kind__name", "notes")
    list_filter = ("date", "kind")


@admin.register(PlantLogKind)
class PlantLogKindAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class PlantInlineBase(admin.TabularInline):
    extra = 0


class PlantImageInline(PlantInlineBase):
    model = PlantImage


class PlantLogInline(PlantInlineBase):
    model = PlantLog


@admin.register(Plant)
class PlantAdmin(admin.GISModelAdmin):
    """Admin inline for Plant model."""

    model = Plant

    autocomplete_fields = ("genus", "species", "variety")
    inlines = [PlantImageInline, PlantLogInline]


@admin.register(Zone)
class ZoneAdmin(admin.GISModelAdmin):
    """Admin inline for Zone model."""

    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ZoneKind)
class ZoneKindAdmin(admin.ModelAdmin):
    """Admin inline for ZoneKind model."""

    list_display = ("name",)
    search_fields = ("name",)
