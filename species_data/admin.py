from django.contrib import admin
from .models import (
    Source,
    SourceType,
    GrowthHabit,
    ClimateZone,
    HumanUse,
    EcologicalRole,
    SoilPreference,
    PropagationMethod,
    # FamilyGrowthHabit,
    # GenusGrowthHabit,
    SpeciesGrowthHabit,
    # FamilyClimateZone,
    # GenusClimateZone,
    SpeciesClimateZone,
    # FamilyHumanUse,
    # GenusHumanUse,
    SpeciesHumanUse,
    # FamilyEcologicalRole,
    # GenusEcologicalRole,
    SpeciesEcologicalRole,
    # FamilySoilPreference,
    # GenusSoilPreference,
    SpeciesSoilPreference,
    SpeciesPropagationMethod,
    # FamilyProperties,
    # GenusProperties,
    SpeciesProperties,
)


@admin.register(SourceType)
class SourceTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "url")
    list_filter = ("source_type",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(GrowthHabit)
class GrowthHabitAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(ClimateZone)
class ClimateZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "main_group", "seasonal_precipitation", "heat_level")
    search_fields = ("name",)
    list_filter = ("main_group", "seasonal_precipitation", "heat_level")


@admin.register(HumanUse)
class HumanUseAdmin(admin.ModelAdmin):
    list_display = ("name", "use_type", "description")
    search_fields = ("name", "description")
    list_filter = ("use_type",)


@admin.register(EcologicalRole)
class EcologicalRoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(SoilPreference)
class SoilPreferenceAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(PropagationMethod)
class PropagationMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


# Inline Admins for through models
class CategoryInlineBase(admin.TabularInline):
    extra = 0
    autocomplete_fields = ("source",)


# class FamilyGrowthHabitInline(CategoryInlineBase):
#     model = FamilyGrowthHabit


# class GenusGrowthHabitInline(CategoryInlineBase):
#     model = GenusGrowthHabit


class SpeciesGrowthHabitInline(CategoryInlineBase):
    model = SpeciesGrowthHabit


# class FamilyClimateZoneInline(CategoryInlineBase):
#     model = FamilyClimateZone


# class GenusClimateZoneInline(CategoryInlineBase):
#     model = GenusClimateZone


class SpeciesClimateZoneInline(CategoryInlineBase):
    model = SpeciesClimateZone


# class FamilyHumanUseInline(CategoryInlineBase):
#     model = FamilyHumanUse


# class GenusHumanUseInline(CategoryInlineBase):
#     model = GenusHumanUse


class SpeciesHumanUseInline(CategoryInlineBase):
    model = SpeciesHumanUse


# class FamilyEcologicalRoleInline(CategoryInlineBase):
#     model = FamilyEcologicalRole


# class GenusEcologicalRoleInline(CategoryInlineBase):
#     model = GenusEcologicalRole


class SpeciesEcologicalRoleInline(CategoryInlineBase):
    model = SpeciesEcologicalRole


# class FamilySoilPreferenceInline(CategoryInlineBase):
#     model = FamilySoilPreference

# class GenusSoilPreferenceInline(CategoryInlineBase):
#     model = GenusSoilPreference


class SpeciesSoilPreferenceInline(CategoryInlineBase):
    model = SpeciesSoilPreference


class SpeciesPropagationMethodInline(CategoryInlineBase):
    model = SpeciesPropagationMethod


_autocomplete_source_fields = [
    "height_source",
    "width_source",
    "soil_acidity_source",
    "production_start_source",
    "production_peak_source",
    "lifetime_source",
]


# @admin.register(FamilyProperties)
# class FamilyPropertiesAdmin(admin.ModelAdmin):
#     inlines = [
#         FamilyGrowthHabitInline,
#         FamilyClimateZoneInline,
#         FamilyHumanUseInline,
#         FamilyEcologicalRoleInline,
#         FamilySoilPreferenceInline,
#         FamilyLightPreferenceInline,
#     ]
#     list_display = ("family",)
#     search_fields = ("family__latin_name", "family__common_names__name")
#     autocomplete_fields = ["family"] + _autocomplete_source_fields


# @admin.register(GenusProperties)
# class GenusPropertiesAdmin(admin.ModelAdmin):
#     inlines = [
#         GenusGrowthHabitInline,
#         GenusClimateZoneInline,
#         GenusHumanUseInline,
#         GenusEcologicalRoleInline,
#         GenusSoilPreferenceInline,
#         GenusLightPreferenceInline,
#     ]
#     list_display = ("genus",)
#     search_fields = (
#         "genus__latin_name",
#         "genus__common_names__name",
#         "genus__family__latin_name",
#         "genus__family__common_names__name",
#     )
#     autocomplete_fields = ["genus"] + _autocomplete_source_fields


@admin.register(SpeciesProperties)
class SpeciesPropertiesAdmin(admin.ModelAdmin):
    list_display = ("species",)

    inlines = [
        SpeciesGrowthHabitInline,
        SpeciesClimateZoneInline,
        SpeciesHumanUseInline,
        SpeciesEcologicalRoleInline,
        SpeciesSoilPreferenceInline,
        SpeciesPropagationMethodInline,
    ]
    search_fields = (
        "species__latin_name",
        "species__common_names__name",
        "species__genus__latin_name",
        "species__genus__common_names__name",
        "species__genus__family__latin_name",
        "species__genus__family__common_names__name",
    )
    autocomplete_fields = ["species"] + _autocomplete_source_fields

    list_filter = (
        "growth_habits",
        "climate_zones",
        "human_uses",
        "ecological_roles",
        "soil_preferences",
        "propagation_methods",
    )
    list_select_related = ("species",)
