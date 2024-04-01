from django.contrib import admin
from .models import (
    Family,
    Genus,
    Species,
    FamilyCommonName,
    GenusCommonName,
    SpeciesCommonName,
    Variety,
)


class FamilyCommonNameInline(admin.TabularInline):
    """Inline admin for family common names."""

    model = FamilyCommonName
    extra = 1


class GenusCommonNameInline(admin.TabularInline):
    """Inline admin for genus common names."""

    model = GenusCommonName
    extra = 1


class SpeciesCommonNameInline(admin.TabularInline):
    """Inline admin for species common names."""

    model = SpeciesCommonName
    extra = 1


class VarietyInline(admin.TabularInline):
    """Inline admin for species varieties."""

    model = Variety
    extra = 1


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    """Admin interface for the Family model."""

    list_display = ("latin_name",)
    inlines = [FamilyCommonNameInline]


@admin.register(Genus)
class GenusAdmin(admin.ModelAdmin):
    """Admin interface for the Genus model."""

    list_display = ("latin_name", "family")
    list_filter = ("family",)
    search_fields = ("latin_name", "family__latin_name")
    inlines = [GenusCommonNameInline]


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    """Admin interface for the Species model."""

    list_display = ("latin_name",)
    inlines = [SpeciesCommonNameInline, VarietyInline]
