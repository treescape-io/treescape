from django.contrib.gis import admin

from forest_designs.models.state import PlantState, PlantStateTransition

from .models import (
    Plant,
    PlantImage,
    PlantImageKind,
    PlantLog,
    PlantLogKind,
    Zone,
    ZoneKind,
)


class KindAdminBase(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    list_display = ("plant", "date", "kind")
    search_fields = ("plant__name", "kind__name")
    list_filter = ("date", "kind")


@admin.register(PlantImageKind)
class PlantImageKindAdmin(KindAdminBase):
    pass


@admin.register(PlantLog)
class PlantLogAdmin(admin.ModelAdmin):
    list_display = ("plant", "date", "kind", "notes")
    search_fields = ("plant__name", "kind__name", "notes")
    list_filter = ("date", "kind")


@admin.register(PlantLogKind)
class PlantLogKindAdmin(KindAdminBase):
    pass


@admin.register(PlantState)
class PlantStateAdmin(KindAdminBase):
    pass


class PlantInlineBase(admin.TabularInline):
    extra = 0


class PlantStateTransitionAdmin(PlantInlineBase):
    model = PlantStateTransition


class PlantImageInline(PlantInlineBase):
    model = PlantImage


class PlantLogInline(PlantInlineBase):
    model = PlantLog


@admin.register(Plant)
class PlantAdmin(admin.GISModelAdmin):
    """Admin inline for Plant model."""

    model = Plant

    autocomplete_fields = ("genus", "species", "variety")
    inlines = [PlantImageInline, PlantStateTransitionAdmin, PlantLogInline]


@admin.register(Zone)
class ZoneAdmin(admin.GISModelAdmin):
    """Admin inline for Zone model."""

    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ZoneKind)
class ZoneKindAdmin(KindAdminBase):
    """Admin inline for ZoneKind model."""

    pass
