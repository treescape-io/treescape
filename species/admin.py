from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.utils.translation import get_language

from species.exceptions import EnrichmentException
from .models import (
    Family,
    Genus,
    Species,
    FamilyCommonName,
    GenusCommonName,
    SpeciesCommonName,
    Variety,
)


# Define a function to retrieve the common name based on the current language.
def get_common_name(obj, model_common_name):
    common_names = model_common_name.objects.filter(
        language=get_language(), **{obj.__class__.__name__.lower(): obj}
    )
    if common_names.exists():
        return common_names.first().name

    # Not available.
    return ""


class FamilyCommonNameInline(admin.TabularInline):
    model = FamilyCommonName
    extra = 0


class GenusCommonNameInline(admin.TabularInline):
    model = GenusCommonName
    extra = 0


class SpeciesCommonNameInline(admin.TabularInline):
    model = SpeciesCommonName
    extra = 0


class VarietyInline(admin.TabularInline):
    model = Variety
    extra = 0


class SpeciesAdminBase(admin.ModelAdmin):
    readonly_fields = ["gbif_id"]

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            return fields
        return ["latin_name"]

    def get_inlines(self, request, obj=None):
        if obj:
            return super().get_inlines(request, obj)  # type: ignore
        return []

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({"show_save": False, "show_save_and_add_another": False})
        return super().add_view(request, form_url, extra_context)  # type: ignore


@admin.register(Family)
class FamilyAdmin(SpeciesAdminBase):
    list_display = ("latin_name", "common_name")
    inlines = [FamilyCommonNameInline]
    search_fields = ["latin_name", "common_names__name"]

    def common_name(self, obj):
        return get_common_name(obj, FamilyCommonName)

    common_name.short_description = _("Common Name")


@admin.register(Genus)
class GenusAdmin(SpeciesAdminBase):
    list_display = ("latin_name", "family", "common_name")
    list_filter = ("family",)
    search_fields = ["latin_name", "common_names__name", "family__latin_name"]
    inlines = [GenusCommonNameInline]

    def common_name(self, obj):
        return get_common_name(obj, GenusCommonName)

    common_name.short_description = _("Common Name")


@admin.register(Species)
class SpeciesAdmin(SpeciesAdminBase):
    # Temporarily disable common name
    list_display = ("latin_name", "genus_family_link")
    list_filter = ("genus__family", "genus")
    search_fields = [
        "latin_name",
        "common_names__name",
        "genus__common_names__name",
        "genus__family__common_names__name",
        "genus__latin_name",
        "genus__family__latin_name",
    ]
    inlines = [SpeciesCommonNameInline, VarietyInline]

    def genus_family_link(self, obj):
        genus_url = reverse("admin:species_genus_change", args=[obj.genus.pk])
        family_url = reverse("admin:species_family_change", args=[obj.genus.family.pk])
        return format_html(
            '<a href="{}">{}</a> / <a href="{}">{}</a>',
            genus_url,
            obj.genus.latin_name,
            family_url,
            obj.genus.family.latin_name,
        )

    genus_family_link.short_description = _("Genus / Family")

    def common_name(self, obj):
        return get_common_name(obj, SpeciesCommonName)

    common_name.short_description = _("Common Name")
