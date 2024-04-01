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


class SpeciesAdminBase(admin.ModelAdmin):
    """Base class for species related admins."""

    readonly_fields = ["gbif_id"]

    def get_fields(self, request, obj=None):
        if obj:
            # Updating existing object
            return super().get_fields(request, obj)

        # When creating species, only set latin name field.
        return ["latin_name"]

    def get_inlines(self, request, obj=None):
        if obj:
            # Only show inlines once object is created
            return super().get_inlines(request, obj)  # type: ignore

        return []

    def add_view(self, request, form_url="", extra_context=None):
        if not extra_context:
            extra_context = {}

        extra_context.update({"show_save": False, "show_save_and_add_another": False})

        return super().add_view(request, form_url, extra_context)  # type: ignore

    def save_model(self, request, obj, form, change):
        if not change:
            # Enrich before saving.
            obj.enrich_species_data()

        super().save_model(request, obj, form, change)


@admin.register(Family)
class FamilyAdmin(SpeciesAdminBase):
    """Admin interface for the Family model."""

    list_display = ("latin_name",)
    inlines = [FamilyCommonNameInline]


@admin.register(Genus)
class GenusAdmin(SpeciesAdminBase):
    """Admin interface for the Genus model."""

    list_display = ("latin_name", "family")
    list_filter = ("family",)
    search_fields = ("latin_name", "family__latin_name")
    inlines = [GenusCommonNameInline]


@admin.register(Species)
class SpeciesAdmin(SpeciesAdminBase):
    """Admin interface for the Species model."""

    list_display = ("latin_name",)
    inlines = [SpeciesCommonNameInline, VarietyInline]
