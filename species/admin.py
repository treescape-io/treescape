from django.contrib import admin
from .models import Family, Genus, Species, SpeciesCommonName, Variety


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    """Admin interface for Family."""

    list_display = ("latin_name",)
    search_fields = ("latin_name",)


@admin.register(Genus)
class GenusAdmin(admin.ModelAdmin):
    """Admin interface for Genus."""

    list_display = ("latin_name", "family")
    list_filter = ("family",)
    search_fields = ("latin_name", "family__latin_name")
    autocomplete_fields = ["family"]


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    """Admin interface for Species."""

    list_display = ("latin_name", "genus")
    list_filter = ("genus", "genus__family")
    search_fields = ("latin_name", "genus__latin_name", "genus__family__latin_name")
    autocomplete_fields = ["genus"]


@admin.register(SpeciesCommonName)
class SpeciesCommonNameAdmin(admin.ModelAdmin):
    """Admin interface for SpeciesCommonName."""

    list_display = ("name", "language", "species")
    list_filter = ("language", "species", "species__genus__family")
    search_fields = (
        "name",
        "species__latin_name",
        "species__genus__latin_name",
        "species__genus__family__latin_name",
    )
    autocomplete_fields = ["species"]


@admin.register(Variety)
class VarietyAdmin(admin.ModelAdmin):
    """Admin interface for Variety."""

    list_display = ("name", "species")
    list_filter = ("species", "species__genus__family")
    search_fields = (
        "name",
        "species__latin_name",
        "species__genus__latin_name",
        "species__genus__family__latin_name",
    )
    autocomplete_fields = ["species"]
