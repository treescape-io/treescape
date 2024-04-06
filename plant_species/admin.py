from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from .models import (
    Family,
    Genus,
    Species,
    FamilyCommonName,
    GenusCommonName,
    SpeciesCommonName,
    SpeciesVariety,
)


class CommonNameInlineBase(admin.TabularInline):
    extra = 0


class FamilyCommonNameInline(CommonNameInlineBase):
    model = FamilyCommonName


class GenusCommonNameInline(CommonNameInlineBase):
    model = GenusCommonName


class SpeciesCommonNameInline(CommonNameInlineBase):
    model = SpeciesCommonName


class VarietyInline(admin.TabularInline):
    model = SpeciesVariety


class SpeciesAdminBase(admin.ModelAdmin):
    save_on_top = True
    readonly_fields = ("gbif_link", "get_image_html")
    exclude = ("gbif_id",)
    list_per_page = 5

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


@admin.register(SpeciesVariety)
class SpeciesVarietyAdmin(admin.ModelAdmin):
    list_display = ("name", "species")
    list_display_filter = ("species__family",)
    autocomplete_fields = ("species",)
    search_fields = (
        "name",
        "species__latin_name",
        "species__common_names__name",
        "species__genus__latin_name",
        "species__genus__common_names__name",
    )


@admin.register(Family)
class FamilyAdmin(SpeciesAdminBase):
    list_display = ("latin_name", "get_common_name", "gbif_link")
    inlines = [FamilyCommonNameInline]
    search_fields = ["latin_name", "common_names__name"]


@admin.register(Genus)
class GenusAdmin(SpeciesAdminBase):
    list_display = ("latin_name", "family", "get_common_name", "gbif_link")
    list_filter = ("family",)
    search_fields = ["latin_name", "common_names__name", "family__latin_name"]
    inlines = [GenusCommonNameInline]
    autocomplete_fields = ("family",)


@admin.register(Species)
class SpeciesAdmin(SpeciesAdminBase):
    list_display = (
        "get_image_html",
        "latin_name",
        "get_common_name",
        "genus_family_link",
        "gbif_link",
    )
    list_display_links = ("get_image_html", "latin_name", "get_common_name")
    list_select_related = ("genus",)
    list_filter = ("genus__family",)
    search_fields = [
        "latin_name",
        "common_names__name",
        "genus__common_names__name",
        "genus__family__common_names__name",
        "genus__latin_name",
        "genus__family__latin_name",
    ]
    autocomplete_fields = ("genus",)
    inlines = [SpeciesCommonNameInline, VarietyInline]

    def genus_family_link(self, obj):
        genus_url = reverse("admin:plant_species_genus_change", args=[obj.genus.pk])
        family_url = reverse(
            "admin:plant_species_family_change", args=[obj.genus.family.pk]
        )
        return format_html(
            '<a href="{}">{}</a> / <a href="{}">{}</a>',
            genus_url,
            obj.genus.latin_name,
            family_url,
            obj.genus.family.latin_name,
        )

    genus_family_link.short_description = _("Genus / Family")
